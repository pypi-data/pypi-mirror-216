from datetime import datetime
import time
from typing import List, Optional

from click import ClickException, confirm

from anyscale.cli_logger import LogsLogger
from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.client.openapi_client.models.create_experimental_workspace import (
    CreateExperimentalWorkspace,
)
from anyscale.client.openapi_client.models.session_state import SessionState
from anyscale.cluster_env import get_default_cluster_env_build
from anyscale.controllers.base_controller import BaseController
from anyscale.project import get_default_project
from anyscale.sdk.anyscale_client.models.compute_node_type import ComputeNodeType
from anyscale.sdk.anyscale_client.models.compute_template_query import (
    ComputeTemplateQuery,
)
from anyscale.sdk.anyscale_client.models.create_cluster_compute import (
    CreateClusterCompute,
)
from anyscale.sdk.anyscale_client.models.create_cluster_compute_config import (
    CreateClusterComputeConfig,
)
from anyscale.util import get_endpoint


POLL_INTERVAL_SECONDS = 10
WORKSPACE_VERIFICATION_TIMEOUT_MINUTES = 10

# default values for cluster compute config
MAXIMUM_UPTIME_MINUTES = 15
IDLE_TERMINATION_MINUTES = 5
HEAD_NODE_TYPE_AWS = "m5.xlarge"
HEAD_NODE_TYPE_GCP = "n1-standard-2"


class CloudFunctionalVerificationController(BaseController):
    def __init__(
        self, log: Optional[LogsLogger] = None, initialize_auth_api_client: bool = True,
    ):
        if log is None:
            log = LogsLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    @staticmethod
    def get_head_node_type(cloud_provider: CloudProviders) -> str:
        """
        Get the default head node type for the given cloud provider.
        """
        if cloud_provider == CloudProviders.AWS:
            return HEAD_NODE_TYPE_AWS
        elif cloud_provider == CloudProviders.GCP:
            return HEAD_NODE_TYPE_GCP
        raise ClickException(f"Unsupported cloud provider: {cloud_provider}")

    def get_or_create_cluster_compute(
        self, cloud_id: str, cloud_provider: CloudProviders
    ) -> str:
        """
        Get or create a cluster compute for cloud functional verification
        """
        cluster_compute_name = f"functional_verification_{cloud_id}"

        cluster_computes = self.api_client.search_compute_templates_api_v2_compute_templates_search_post(
            ComputeTemplateQuery(
                orgwide=True,
                name={"equals": cluster_compute_name},
                include_anonymous=True,
            )
        ).results
        if len(cluster_computes) > 0:
            return cluster_computes[0].id

        head_node_instance_type = self.get_head_node_type(cloud_provider)
        # no cluster compute found, create one
        cluster_compute_config = CreateClusterComputeConfig(
            cloud_id=cloud_id,
            max_workers=0,
            allowed_azs=["any"],
            head_node_type=ComputeNodeType(
                name="head_node_type", instance_type=head_node_instance_type,
            ),
            maximum_uptime_minutes=MAXIMUM_UPTIME_MINUTES,
            idle_termination_minutes=IDLE_TERMINATION_MINUTES,
            worker_node_types=[],
        )
        if cloud_provider == CloudProviders.AWS:
            cluster_compute_config.aws_advanced_configurations_json = {
                "TagSpecifications": [
                    {
                        "ResourceType": "instance",
                        "Tags": [
                            {"Key": "cloud_functional_verification", "Value": cloud_id,}
                        ],
                    }
                ]
            }
        elif cloud_provider == CloudProviders.GCP:
            cluster_compute_config.gcp_advanced_configurations_json = {
                "instance_properties": {
                    "labels": {"cloud_functional_verification": cloud_id},
                }
            }

        cluster_compute = self.anyscale_api_client.create_cluster_compute(
            CreateClusterCompute(
                name=cluster_compute_name,
                config=cluster_compute_config,
                anonymous=True,
            )
        ).result
        return cluster_compute.id

    def verify_workspace(self, cloud_id: str, cloud_provider: CloudProviders) -> bool:
        """
        Verifies that the workspace is setup correctly on the given cloud
        """
        self.log.info("Starting workspace verification...")
        confirm(
            "Workspace verification will create a workspace on the cloud. \n"
            f"This will spin up a {self.get_head_node_type(cloud_provider)} instance for about 5 to 10 minutes and will incur costs. \n"
            "The workspace will be terminated after verification. Do you want to continue?",
            abort=True,
        )
        try:
            with self.log.spinner("Preparing to create workspace..."):
                cluster_compute_id = self.get_or_create_cluster_compute(
                    cloud_id, cloud_provider
                )

                cluster_env_build_id = get_default_cluster_env_build(
                    self.api_client, self.anyscale_api_client
                ).id

                project_id = get_default_project(
                    self.api_client, self.anyscale_api_client, parent_cloud_id=cloud_id
                ).id
        except ClickException as e:
            self.log.error(f"Failed to prepare workspace: {e}")
            return False

        try:
            with self.log.spinner("Creating workspace..."):

                create_workspace_arg = CreateExperimentalWorkspace(
                    name=f"workspace_functional_verification_{cloud_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    description=f"workspace for cloud {cloud_id} functional verification",
                    project_id=project_id,
                    cloud_id=cloud_id,
                    compute_config_id=cluster_compute_id,
                    cluster_environment_build_id=cluster_env_build_id,
                    idle_timeout_minutes=IDLE_TERMINATION_MINUTES,
                )

                workspace_response = self.api_client.create_workspace_api_v2_experimental_workspaces_post(
                    create_workspace_arg
                )
        except ClickException as e:
            self.log.error(f"Failed to create workspace: {e}")
            return False

        workspace_id = str(workspace_response.result.id)
        cluster_id = str(workspace_response.result.cluster_id)
        url = get_endpoint(f"/workspaces/{workspace_id}/{cluster_id}")
        self.log.info(f"Workspace created at {url}")
        verification_result = self.check_workspace_until_active(workspace_id, url)
        if verification_result:
            self.log.info("Workspace verification succeeded.")
        else:
            self.log.error(
                f"Workspace verification failed. Please check errors at {url}"
            )

        # terminate workspace by terminating the cluster
        try:
            self.anyscale_api_client.terminate_cluster(cluster_id, {})
        except ClickException as e:
            # even if we fail to terminate the cluster, it will be terminated automatically with maximum uptime speicified
            self.log.error(f"Failed to terminate workspace: {e}")
        return verification_result

    def check_workspace_until_active(self, workspace_id: str, url: str):
        self.log.info(
            "Note it may take about 5 to 10 minutes to create a workspace for the first time on a cloud."
        )
        with self.log.spinner("Waiting for workspace to be active..."):
            start_time = time.time()
            end_time = start_time + WORKSPACE_VERIFICATION_TIMEOUT_MINUTES * 60
            while time.time() < end_time:
                time.sleep(POLL_INTERVAL_SECONDS)
                try:
                    workspace = self.api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get(
                        workspace_id
                    ).result
                except ClickException as e:
                    self.log.error(f"Failed to get workspace status: {e}")
                    return False
                self.log.info(f"Workspace status: {workspace.state}")
                if workspace.state == SessionState.RUNNING:
                    return True
        self.log.error(f"Timeout when creating workspace, please check errors at {url}")
        return False

    def start_verification(
        self,
        cloud_id: str,
        cloud_provider: CloudProviders,
        functions_to_verify: List[str],
    ) -> bool:
        # TODO (congding): parallelize the verification
        # TODO (congding): add service
        verification_results: List[bool] = []
        for function in functions_to_verify:
            if function == "workspace":
                workspace_verification_result = self.verify_workspace(
                    cloud_id, cloud_provider
                )
                verification_results.append(workspace_verification_result)
        return all(verification_results)
