import json
import os
from os import path
import shlex
import subprocess
from typing import Any, Dict, List, Optional, Sequence, Union

import click
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import (
    AppConfig,
    Build,
    ComputeTemplateConfig,
    CreateComputeTemplate,
    Session,
    StopSessionOptions,
)
from anyscale.cluster_config import get_cluster_config
from anyscale.controllers.base_controller import BaseController
from anyscale.project import (
    get_and_validate_project_id,
    get_project_id,
    get_project_session,
    get_project_sessions,
    load_project_or_throw,
)
from anyscale.sdk.anyscale_client import StartSessionOptions, UpdateSession
from anyscale.sdk.anyscale_client.models.create_cluster import CreateCluster
from anyscale.shared_anyscale_utils.util import get_container_name, slugify
from anyscale.util import (
    canonicalize_remote_location,
    get_endpoint,
    get_working_dir,
    wait_for_session_start,
)
from anyscale.utils.aws_credentials_util import (
    get_credentials_as_env_vars_from_cluster_config,
)
from anyscale.utils.env_utils import set_env
from anyscale.utils.imports.all import try_import_ray
from anyscale.utils.name_utils import gen_valid_name


def get_head_node_ip(cluster_config: Union[Dict[str, Any], str]) -> Any:
    try_import_ray()
    from ray.autoscaler.sdk import get_head_node_ip

    return get_head_node_ip(cluster_config)


def rsync(*args: Any, **kwargs: Any) -> None:
    try_import_ray()
    from ray.autoscaler.sdk import rsync as ray_rsync

    ray_rsync(*args, **kwargs)


class SessionController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    def stop(
        self,
        session_name: Optional[str],
        delete: bool,
        workers_only: bool,
        keep_min_workers: bool,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        sessions = get_project_sessions(
            project_id, session_name, self.api_client, all_active_states=True
        )

        if not session_name and len(sessions) > 1:
            raise click.ClickException(
                "Multiple active sessions: {}\n"
                "Please specify the one you want to stop with --cluster-name.".format(
                    [session.name for session in sessions]
                )
            )

        for session in sessions:
            # Stop the session and mark it as stopped in the database.
            self.api_client.stop_session_api_v2_sessions_session_id_stop_post(
                session.id,
                StopSessionOptions(
                    terminate=True,
                    workers_only=workers_only,
                    keep_min_workers=keep_min_workers,
                    delete=delete,
                ),
            )

        session_names = [session.name for session in sessions]
        session_names_str = ", ".join(session_names)
        url = get_endpoint(f"/projects/{project_id}")
        self.log.info(
            f"Session {session_names_str} shutting down. View progress at {url}"
        )

    def start(
        self,
        session_name: Optional[str],
        build_id: Optional[str],
        build_identifier: Optional[str],
        compute_config: str,
        idle_timeout: Optional[int],
        sync_files: bool,
    ) -> None:
        if sync_files:
            raise click.ClickException(
                "--sync-files has been deprecated and `anyscale start` will no longer ensure files "
                "synced to the working directory of the head node will also be synced on the workers."
            )
        message = (
            "Warning: `anyscale start` has been deprecated. Please try "
            'using `ray.init("anyscale://cluster_name")` for your use case and let the Anyscale team '
            "know if you are having any issues."
        )
        self.log.warning(message)

        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session_name = self._get_or_generate_session_name(session_name, project_id)

        assert (
            build_id or build_identifier
        ), "--build-id or --build-identifier must be specified."
        if not build_id and build_identifier:
            build_id = self._get_build_id_from_build_identifier(
                build_identifier, project_id
            )
        assert build_id  # for mypy

        compute_template_id = self._register_compute_config(compute_config, project_id)

        session = self._create_or_update_session_data(
            session_name, project_id, build_id, compute_template_id, idle_timeout
        )
        self.anyscale_api_client.start_session(
            session.id,
            StartSessionOptions(
                build_id=build_id, compute_template_id=compute_template_id
            ),
        )

        wait_for_session_start(project_id, session_name, self.api_client)
        url = get_endpoint(f"/projects/{project_id}/clusters/{session.id}")
        print(f"Session {session_name} finished starting. View at {url}")

    def ssh(  # noqa: PLR0912, PLR0913
        self,
        session_name: str,
        ssh_option: Sequence[str],
        worker_node_id: Optional[str],
        worker_node_ip: Optional[str],
        force_head_node: bool,
        project_id: Optional[str],
        cmd: Optional[str] = None,
    ) -> None:

        config_path = "/home/ray/ray_bootstrap_config.yaml"
        on_head_node = path.exists(config_path)

        ssh_to_head = worker_node_id is None and worker_node_ip is None

        if force_head_node and ssh_to_head:
            raise click.ClickException(
                "Can't force head node if not sshing to a worker_node."
            )

        if worker_node_id is not None and worker_node_ip is not None:
            raise click.ClickException(
                "A worker node id and worker node ip cannot both be set at once."
            )

        if force_head_node or (on_head_node and (worker_node_id or worker_node_ip)):
            # On the head node
            print("SSHing from head node to worker node.")

            # Import ray where it's needed here to avoid making ray a
            # regular dependency of the CLI. This should only execute on
            # a head node where we can be confident ray will already
            # be installed.
            ray = try_import_ray()

            with open(config_path) as f:
                config_dict = yaml.safe_load(f)

            try:
                ssh_user = config_dict["auth"]["ssh_user"]
                ssh_key_path = config_dict["auth"]["ssh_private_key"]
                container_name = config_dict["docker"]["container_name"]
            except ValueError as e:
                raise click.ClickException(
                    f"Could not parse ~/ray_bootstrap_config.yaml: {e}"
                )

            if worker_node_ip is not None:
                node_ip = worker_node_ip
            elif worker_node_id is not None:
                ray.init(address="auto")
                nodes = ray.nodes()
                node_info = next(
                    (node for node in nodes if node.get("NodeID") == worker_node_id),
                    None,
                )
                if node_info is None:
                    raise click.ClickException(
                        f"Could not find a worker node with id {worker_node_id}."
                    )
                node_ip = node_info.get("NodeManagerAddress")

            ssh_command = (
                ["ssh"]
                + list(ssh_option)
                + ["-tt", "-i", ssh_key_path]
                + [f"{ssh_user}@{node_ip}"]
                + [f"docker exec -it {container_name} sh -c 'which bash && bash || sh'"]
            )
        else:
            # On a laptop
            project_id = get_and_validate_project_id(
                project_id=project_id,
                project_name=None,
                parent_cloud_id=None,
                api_client=self.api_client,
                anyscale_api_client=self.anyscale_api_client,
            )
            session = get_project_session(project_id, session_name, self.api_client)

            cluster_config = get_cluster_config(
                session_name,
                self.api_client,
                disable_project_sync=True,
                project_id=project_id,
            )

            head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
                session.id
            ).result.head_ip

            ssh_user = cluster_config["auth"]["ssh_user"]
            key_path = cluster_config["auth"]["ssh_private_key"]
            container_name = get_container_name(cluster_config)

            base_ssh_command = (
                ["ssh"]
                + list(ssh_option)
                + ["-tt", "-i", key_path]
                + [f"{ssh_user}@{head_ip}"]
            )
            if cmd:
                command = shlex.quote(cmd)
            else:
                command = shlex.quote("which bash && bash || sh")

            if ssh_to_head:
                ssh_command = base_ssh_command + (
                    [f"docker exec -it {container_name} sh -c {command}"]
                    if container_name
                    else []
                )
            else:
                if not container_name:
                    raise click.ClickException(
                        "Cannot ssh to a worker node if this cluster has no container."
                    )
                # Don't use the ssh_options for the second ssh command because
                # they probably refer to files that exist on the laptop but not
                # the head node.

                if worker_node_id is not None:
                    ssh_flag = f"--worker-node-id {worker_node_id}"
                else:
                    ssh_flag = f"--worker-node-ip {worker_node_ip}"
                ssh_from_head_command = (
                    f"'anyscale ssh {ssh_flag} --force-head-node True'"
                )
                ssh_command = base_ssh_command + (
                    [f"docker exec -it {container_name} sh -c  {ssh_from_head_command}"]
                )

        subprocess.run(ssh_command)

    def pull(
        self,
        session_name: Optional[str] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        config: Optional[str] = None,
        rsync_exclude_override: Optional[List[str]] = None,
    ) -> None:
        project_definition = load_project_or_throw()

        try:
            self.log.info("Collecting files from remote.")
            project_id = get_project_id(project_definition.root)
            cluster_config = get_cluster_config(session_name, self.api_client)
            if rsync_exclude_override is not None:
                cluster_config["rsync_exclude"] = rsync_exclude_override
            directory_name = get_working_dir(
                cluster_config, project_id, self.api_client
            )
            source_directory = f"{directory_name}/"

            aws_credentials = get_credentials_as_env_vars_from_cluster_config(
                cluster_config
            )

            source = canonicalize_remote_location(cluster_config, source, project_id)

            with set_env(**aws_credentials):
                if source and target:
                    target = os.path.expanduser(target)
                    rsync(
                        cluster_config, source=source, target=target, down=True,
                    )
                elif source or target:
                    raise click.ClickException(
                        "Source and target are not both specified. Please either specify both or neither."
                    )
                else:
                    rsync(
                        cluster_config,
                        source=source_directory,
                        target=project_definition.root,
                        down=True,
                    )

            if config:
                session = get_project_session(project_id, session_name, self.api_client)
                resp = self.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                    session.id
                )
                cluster_config = yaml.safe_load(resp.result.config_with_defaults)
                with open(config, "w") as f:
                    yaml.dump(cluster_config, f, default_flow_style=False)

            self.log.info("Pull completed.")

        except Exception as e:  # noqa: BLE001
            print(e)
            raise click.ClickException(str(e))  # type: ignore

    def push(
        self,
        session_name: Optional[str],
        source: Optional[str],
        target: Optional[str],
        config: Optional[str],  # noqa: ARG002
        all_nodes: bool,
        rsync_exclude_override: Optional[List[str]] = None,
    ) -> None:
        if all_nodes:
            raise click.ClickException(
                "The `all_nodes` option is deprecated and will be removed in the future. "
                "Pushing to worker nodes is not reliable since workers may be "
                "added during autoscaling. Going forward, Anyscale will only support syncing "
                "working directory files to the head and workers."
            )

        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session = get_project_session(project_id, session_name, self.api_client)
        session_name = session.name

        cluster_config = get_cluster_config(session_name, self.api_client)
        if rsync_exclude_override is not None:
            cluster_config["rsync_exclude"] = rsync_exclude_override
        target = canonicalize_remote_location(cluster_config, target, project_id)

        aws_credentials = get_credentials_as_env_vars_from_cluster_config(
            cluster_config
        )

        with set_env(**aws_credentials):
            if source and target:
                rsync(
                    cluster_config, source=source, target=target, down=False,
                )
            elif source or target:
                raise click.ClickException(
                    "Source and target are not both specified. Please either specify both or neither."
                )
            else:
                rsync(
                    cluster_config, source=None, target=None, down=False,
                )

        url = get_endpoint(f"/projects/{project_id}/clusters/{session.id}")
        self.log.info(f"Pushed to session {session_name}. View at {url}")

    # Helpers

    def _get_or_generate_session_name(
        self, session_name: Optional[str], project_id: Optional[str]
    ) -> str:
        """
        Return slugified session name if provided, else generate default session name from project id
        """
        assert (
            session_name or project_id
        ), "Either the session_name or project_id must be provided"

        if not session_name:
            session_name = str(
                self.api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(
                    project_id=project_id,
                ).result.name
            )
        else:
            session_name = slugify(session_name)
        assert session_name
        return session_name

    def _register_compute_config(
        self, compute_config_file: str, project_id: str
    ) -> str:
        """
        Register the compute config with Anyscale and get its ID.
        """
        with open(compute_config_file) as f:
            config_dict = json.load(f)
        config_object = ComputeTemplateConfig(**config_dict)
        created_template = self.api_client.create_compute_template_api_v2_compute_templates_post(
            create_compute_template=CreateComputeTemplate(
                name=gen_valid_name("autogenerated-config"),
                project_id=project_id,
                config=config_object,
            )
        ).result
        compute_template_id = str(created_template.id)
        return compute_template_id

    def _create_or_update_session_data(
        self,
        session_name: str,
        project_id: str,
        build_id: str,
        compute_template_id: str,
        idle_timeout: Optional[int],
    ) -> Session:
        """
        Creates new session with app configs if session with `session_name` doesn't
        already exist. Otherwise, update the `idle_timeout` of the existing
        session if provided.
        """
        session_list = self.api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, active_only=False, name=session_name
        ).results

        session_exists = len(session_list) > 0
        if not session_exists:
            # Create a new session if there is no existing session with the givens session_name
            create_session_data = CreateCluster(
                name=session_name,
                project_id=project_id,
                cluster_environment_build_id=build_id,
                cluster_compute_id=compute_template_id,
                idle_timeout_minutes=idle_timeout,
            )
            session = self.anyscale_api_client.create_cluster(
                create_session_data
            ).result
        else:
            # Get the existing session and update the idle_timeout if required
            session = session_list[0]
            if idle_timeout:
                self.anyscale_api_client.update_session(
                    session.id, UpdateSession(idle_timeout=idle_timeout)
                )

        return session

    def _get_build_id_from_build_identifier(
        self, build_identifier: str, project_id: str
    ) -> str:
        # TODO(nikita): App config API should support getting a build ID from the build identifier.
        components = build_identifier.rsplit(":", 1)
        app_config_name = components[0]
        # try catch this
        try:
            app_config_revision = int(components[1]) if len(components) > 1 else None
        except ValueError:
            raise click.ClickException(
                "Invalid build-identifier provided. Please make sure the build identifier is of "
                "the form <app-config-name>:<build-revision>."
            )

        app_config_id = self._get_app_config_id_from_name(app_config_name, project_id)

        builds = self._list_builds(app_config_id)
        if app_config_revision:
            for build in builds:
                if build.revision == app_config_revision:
                    return str(build.id)

            raise click.ClickException(
                "Revision {} of app config '{}' not found.".format(
                    app_config_revision, app_config_name
                )
            )
        else:
            latest_build_revision = -1
            build_to_use = None
            for build in builds:
                if build.revision > latest_build_revision:
                    latest_build_revision = build.revision
                    build_to_use = build

            if not build_to_use:
                raise click.ClickException(
                    "Error finding latest build of app config {}. Please manually "
                    "specify the build version in the build identifier.".format(
                        app_config_name
                    )
                )
            return str(build_to_use.id)

    def _get_app_config_id_from_name(
        self, app_config_name: str, project_id: str
    ) -> str:
        app_configs = self._list_app_configs(project_id)
        for app_config in app_configs:
            if app_config.name == app_config_name:
                return str(app_config.id)

        raise click.ClickException(
            f"Application config '{app_config_name}' not found. "
            + "Available app configs: {}".format(", ".join(a.name for a in app_configs))
        )

    def _list_app_configs(self, project_id: str) -> List[AppConfig]:
        entities = []
        has_more = True
        paging_token = None
        i = 0
        while has_more and i < 100:
            resp = self.anyscale_api_client.list_app_configs(
                project_id=project_id, count=50, paging_token=paging_token
            )
            entities.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = paging_token is not None
            i += 1
        return entities

    def _list_builds(self, app_config_id: str) -> List[Build]:
        entities = []
        has_more = True
        paging_token = None
        i = 0
        while has_more and i < 100:
            resp = self.anyscale_api_client.list_builds(
                app_config_id, count=50, paging_token=paging_token
            )
            entities.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = paging_token is not None
            i += 1
        return entities

    def _resolve_session(
        self, session_name: str, project_name: Optional[str] = None
    ) -> Session:
        """
        Resolves a session by name.
        This is distinct from  `anyscale.project.get_project_session` because:
        1. we rely on project names instead of ids
        2. we allow non-active sessions to be resolved

        Raises an exception if the session does not exist.

        Params
        session_name - name of the session
        project_name - optional project name that the session is in;
                       if absent, we use the workspace's project
        """
        if project_name:
            projects = self.api_client.list_projects_api_v2_projects_get().results
            project = next(
                project for project in projects if project.name == project_name
            )
            project_id = project.id
        else:
            project_definition = load_project_or_throw()
            project_id = get_project_id(project_definition.root)

        sessions_list = self.api_client.list_sessions_api_v2_sessions_get(
            project_id, name=session_name
        ).results

        if len(sessions_list) == 0:
            raise click.ClickException(
                f"No session found with name {session_name} in project {project_id}"
            )

        return sessions_list[0]
