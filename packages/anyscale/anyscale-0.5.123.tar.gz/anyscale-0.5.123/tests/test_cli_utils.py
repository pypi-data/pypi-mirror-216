import datetime
from unittest.mock import Mock, patch

from click.exceptions import ClickException
from freezegun import freeze_time
import pytest

from anyscale.client.openapi_client import Session, SessionListResponse
from anyscale.client.openapi_client.models.project import Project
from anyscale.util import (
    canonicalize_remote_location,
    credentials_check_sanity,
    deserialize_datetime,
    get_project_directory_name,
    get_working_dir,
    wait_for_session_start,
)


@pytest.mark.parametrize(
    ("working_dir", "remote_location", "result"),  # type: ignore
    [
        ("test-working-dir", "/a/b/c", "/a/b/c"),
        ("~/test-working-dir", "/root/a/b/c", "~/a/b/c"),
        ("/root/test-working-dir", "~/a/b/c", "/root/a/b/c"),
        ("/root/test-working-dir", "/root/a/b/c", "/root/a/b/c"),
        ("~/test-working-dir", "~/a/b/c", "~/a/b/c"),
    ],
)
def test_canonicalize_remote_location(working_dir, remote_location, result):
    """Test that canonicalize_remote_location
    changes remote_location from being based
    in "~/" or "/root/" to match working_dir.
    """
    cluster_config = {
        "metadata": {"anyscale": {"working_dir": working_dir}},
        "docker": {"container_name": "test-container-name"},
    }
    project_id = "test-project-id"
    assert (
        canonicalize_remote_location(cluster_config, remote_location, project_id)
        == result
    )

    # Test with "ray" not "root"
    result_ray = result.replace("root", "ray")
    cluster_config["metadata"]["anyscale"]["working_dir"] = working_dir.replace(  # type: ignore
        "root", "ray"
    )
    assert (
        canonicalize_remote_location(
            cluster_config, remote_location.replace("root", "ray"), project_id
        )
        == result_ray
    )


def test_deserialize_datetime() -> None:
    date_str = "2020-07-02T20:16:04.000000+00:00"
    assert deserialize_datetime(date_str) == datetime.datetime(
        2020, 7, 2, 20, 16, 4, tzinfo=datetime.timezone.utc
    )


def test_wait_for_session_start(
    mock_api_client_with_session: Mock, session_test_data: Session
) -> None:
    result = wait_for_session_start(
        session_test_data.project_id, session_test_data.id, mock_api_client_with_session
    )
    assert result == session_test_data.id


def test_wait_for_session_start_error(
    mock_api_client_with_session: Mock, session_start_error_test_data: Session
) -> None:
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_start_error_test_data]
    )
    with pytest.raises(ClickException) as e:
        wait_for_session_start(
            session_start_error_test_data.project_id,
            session_start_error_test_data.id,
            mock_api_client_with_session,
        )

    assert "Error while starting cluster" in e.value.message
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_start_error_test_data.project_id,
        name=session_start_error_test_data.id,
        active_only=False,
    )


def test_wait_for_session_start_terminated(
    mock_api_client_with_session: Mock, session_terminated_test_data: Session
) -> None:
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_terminated_test_data]
    )

    # Mock time so we don't need to wait 30 real time seconds for terminated
    # grace period
    freezer = freeze_time("2023-01-1 12:00:00")
    freezer.start()

    def sleep_mock(*args, **kwargs):
        freezer.stop()

    with patch("time.sleep", sleep_mock), pytest.raises(ClickException) as e:
        wait_for_session_start(
            session_terminated_test_data.project_id,
            session_terminated_test_data.id,
            mock_api_client_with_session,
        )

    assert "Cluster is still in stopped/terminated state" in e.value.message
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_with(
        project_id=session_terminated_test_data.project_id,
        name=session_terminated_test_data.id,
        active_only=False,
    )


def test_wait_for_session_start_terminated_grace_period(
    mock_api_client_with_session: Mock,
    session_terminated_test_data: Session,
    session_test_data: Session,
) -> None:
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_terminated_test_data]
    )
    """
    Tests first iteration of loop with session in terminated state. On next iteration, we update
    the session to be in running state. Since the terminated state happens within the grace period,
    there should be no error (as opposed to test_wait_for_session_start_terminated)
    """

    def sleep_mock(*args, **kwargs):
        mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_with(
            project_id=session_terminated_test_data.project_id,
            name=session_terminated_test_data.id,
            active_only=False,
        )
        # Changed mocked response from terminated to running
        mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
            results=[session_test_data]
        )
        mock_api_client_with_session.reset_mock()

    with patch("time.sleep", sleep_mock):
        result = wait_for_session_start(
            session_terminated_test_data.project_id,
            session_terminated_test_data.id,
            mock_api_client_with_session,
        )

    assert result == session_test_data.id

    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_with(
        project_id=session_test_data.project_id,
        name=session_test_data.id,
        active_only=False,
    )


def test_wait_for_session_start_missing_session(
    mock_api_client_with_session: Mock, session_start_error_test_data: Session
) -> None:
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[]
    )
    with pytest.raises(ClickException) as e:
        wait_for_session_start(
            session_start_error_test_data.project_id,
            session_start_error_test_data.id,
            mock_api_client_with_session,
        )

    assert "Cluster doesn't exist" in e.value.message
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_start_error_test_data.project_id,
        name=session_start_error_test_data.id,
        active_only=False,
    )


def test_get_project_directory_name(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    dir_name = get_project_directory_name(project_test_data.id, mock_api_client)

    assert dir_name == project_test_data.directory_name
    mock_api_client.get_project_api_v2_projects_project_id_get.assert_called_once_with(
        project_test_data.id
    )


def test_get_working_dir(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    working_dir = get_working_dir({}, project_test_data.id, mock_api_client)
    assert working_dir == f"/home/ray/{project_test_data.directory_name}"

    working_dir = get_working_dir(
        {"metadata": {"anyscale": {"working_dir": "test_working_dir"}}},
        project_test_data.id,
        mock_api_client,
    )
    assert working_dir == "test_working_dir"


def test_credentials_check_sanity():
    # valid credentials
    assert credentials_check_sanity("sss_abcdefg1234567")
    assert credentials_check_sanity("aph0_abcdefg1234567")
    assert credentials_check_sanity("ash0_abcdefg1234567")
    assert credentials_check_sanity("sss_this-=!./#should_3$be_a_valid_ToKEn.%")
    assert credentials_check_sanity("aph0_052943312512")

    # wrong or no prefix
    assert not credentials_check_sanity("wrong_abcdefg1234567")
    assert not credentials_check_sanity("withoutanyprefixes")
