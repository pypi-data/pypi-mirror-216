from typing import Iterator, List
from unittest.mock import Mock, patch

from click import ClickException
import pytest

from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.client.openapi_client.models.session_state import SessionState
from anyscale.controllers.cloud_functional_verification_controller import (
    CloudFunctionalVerificationController,
)
from anyscale.sdk.anyscale_client.models.compute_template_query import (
    ComputeTemplateQuery,
)


@pytest.fixture(autouse=True)
def mock_auth_api_client(base_mock_anyscale_api_client: Mock) -> Iterator[None]:
    mock_auth_api_client = Mock(
        api_client=Mock(), anyscale_api_client=base_mock_anyscale_api_client,
    )
    with patch.multiple(
        "anyscale.controllers.base_controller",
        get_auth_api_client=Mock(return_value=mock_auth_api_client),
    ):
        yield


@pytest.mark.parametrize("cloud_provider", [CloudProviders.AWS, CloudProviders.GCP])
@pytest.mark.parametrize("compute_config_exists", [True, False])
def test_get_or_create_cluster_compute(
    compute_config_exists: bool, cloud_provider: CloudProviders,
) -> None:
    mock_cloud_id = "mock_cloud_id"
    mock_cluster_compute_id = "mock_cluster_compute_id"
    mock_api_client = Mock()
    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post = Mock(
        return_value=Mock(
            results=[Mock(id=mock_cluster_compute_id)] if compute_config_exists else []
        )
    )
    mock_anyscale_api_client = Mock()
    mock_anyscale_api_client.create_cluster_compute = Mock(
        return_value=Mock(result=Mock(id=mock_cluster_compute_id))
    )

    funciontal_verification_controller = CloudFunctionalVerificationController()
    funciontal_verification_controller.api_client = mock_api_client
    funciontal_verification_controller.anyscale_api_client = mock_anyscale_api_client
    assert (
        funciontal_verification_controller.get_or_create_cluster_compute(
            mock_cloud_id, cloud_provider
        )
        == mock_cluster_compute_id
    )

    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post.assert_called_with(
        ComputeTemplateQuery(
            orgwide=True,
            name={"equals": f"functional_verification_{mock_cloud_id}"},
            include_anonymous=True,
        )
    )

    if compute_config_exists:
        mock_anyscale_api_client.create_cluster_compute.assert_not_called()
    else:
        mock_anyscale_api_client.create_cluster_compute.assert_called_once()


@pytest.mark.parametrize(
    (
        "workspace_preparation_failed",
        "workspace_creation_failed",
        "verification_result",
        "expected_result",
        "expected_log_message",
    ),
    [
        pytest.param(
            False,
            False,
            True,
            True,
            "Workspace verification succeeded.",
            id="happy-path",
        ),
        pytest.param(
            False,
            False,
            False,
            False,
            "Workspace verification failed.",
            id="workspace-verification-failed",
        ),
        pytest.param(
            False,
            True,
            False,
            False,
            "Failed to create workspace:",
            id="workspace-creation-failed",
        ),
        pytest.param(
            True,
            False,
            False,
            False,
            "Failed to prepare workspace:",
            id="workspace-preparation-failed",
        ),
    ],
)
@pytest.mark.parametrize("cloud_provider", [CloudProviders.AWS, CloudProviders.GCP])
def test_verify_workspace(
    capsys,
    cloud_provider: CloudProviders,
    verification_result: bool,
    workspace_preparation_failed: bool,
    workspace_creation_failed: bool,
    expected_log_message: str,
    expected_result: bool,
):
    mock_cluster_env_build_id = "mock_cluster_env_build_id"
    mock_cluster_compute_id = "mock_cluster_compute_id"
    mock_project_id = "mock_project_id"
    mock_workspace_id = "mock_workspace_id"
    mock_cluster_id = "mock_cluster_id"
    mock_cloud_id = "mock_cloud_id"

    mock_api_client = Mock()
    if workspace_creation_failed:
        mock_api_client.create_workspace_api_v2_experimental_workspaces_post = Mock(
            side_effect=ClickException("mock error")
        )
    else:
        mock_api_client.create_workspace_api_v2_experimental_workspaces_post = Mock(
            return_value=Mock(
                result=Mock(id=mock_workspace_id, cluster_id=mock_cluster_id)
            )
        )
    mock_anyscale_api_client = Mock()
    mock_anyscale_api_client.terminate_cluster = Mock()
    if workspace_preparation_failed:
        mock_get_or_create_cluster_compute = Mock(
            side_effect=ClickException("mock error")
        )
    else:
        mock_get_or_create_cluster_compute = Mock(return_value=mock_cluster_compute_id)

    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller",
        confirm=Mock(),
        get_default_cluster_env_build=Mock(
            return_value=Mock(id=mock_cluster_env_build_id)
        ),
        get_default_project=Mock(return_value=Mock(id=mock_project_id)),
    ), patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        check_workspace_until_active=Mock(return_value=verification_result),
        get_or_create_cluster_compute=mock_get_or_create_cluster_compute,
    ):
        funciontal_verification_controller = CloudFunctionalVerificationController()
        funciontal_verification_controller.api_client = mock_api_client
        funciontal_verification_controller.anyscale_api_client = (
            mock_anyscale_api_client
        )
        assert (
            funciontal_verification_controller.verify_workspace(
                mock_cloud_id, cloud_provider
            )
            == expected_result
        )
        if workspace_preparation_failed:
            mock_api_client.create_workspace_api_v2_experimental_workspaces_post.assert_not_called()
        else:
            mock_api_client.create_workspace_api_v2_experimental_workspaces_post.assert_called_once()

        _, log = capsys.readouterr()
        assert expected_log_message in log


@pytest.mark.parametrize("get_workspace_error", [True, False])
def test_check_workspace_until_active(capsys, get_workspace_error: bool):
    mock_api_client = Mock()
    if get_workspace_error:
        mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get = Mock(
            side_effect=ClickException("mock error")
        )
    else:
        mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get = Mock(
            return_value=Mock(result=Mock(state=SessionState.RUNNING))
        )

    funciontal_verification_controller = CloudFunctionalVerificationController()
    funciontal_verification_controller.api_client = mock_api_client
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller",
        POLL_INTERVAL_SECONDS=0,
    ):
        assert funciontal_verification_controller.check_workspace_until_active(
            "mock_workspace_id", "mock_url"
        ) == (not get_workspace_error)

    _, err = capsys.readouterr()
    assert ("Failed to get workspace status:" in err) == get_workspace_error


def test_check_workspace_until_active_timeout(capsys):
    mock_workspace_id = "mock_workspace_id"
    mock_url = "mock_url"

    funciontal_verification_controller = CloudFunctionalVerificationController()
    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller",
        WORKSPACE_VERIFICATION_TIMEOUT_MINUTES=0,
    ):
        assert (
            funciontal_verification_controller.check_workspace_until_active(
                mock_workspace_id, mock_url
            )
            is False
        )

    _, err = capsys.readouterr()
    assert "Timeout when creating workspace, please check errors at" in err


@pytest.mark.parametrize("verification_result", [True, False])
@pytest.mark.parametrize("cloud_provider", [CloudProviders.AWS, CloudProviders.GCP])
@pytest.mark.parametrize("functions_to_verify", [["workspace"]])
def test_start_verification(
    functions_to_verify: List[str],
    cloud_provider: CloudProviders,
    verification_result: bool,
):
    # TODO (congding): add test case for "service"
    mock_cloud_id = "mock_cloud_id"

    with patch.multiple(
        "anyscale.controllers.cloud_functional_verification_controller.CloudFunctionalVerificationController",
        verify_workspace=Mock(return_value=verification_result),
    ):
        funciontal_verification_controller = CloudFunctionalVerificationController()
        assert (
            funciontal_verification_controller.start_verification(
                mock_cloud_id, cloud_provider, functions_to_verify
            )
            == verification_result
        )
