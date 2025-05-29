import pytest
from unittest.mock import patch, MagicMock
from services.docker_client import DockerClient
from models.exceptions import NoDataFoundException


@patch('services.docker_client.docker.from_env')
def test_list_images_success(mock_from_env):
    mock_client = MagicMock()
    mock_image = MagicMock()
    mock_image.id = "12345"
    mock_image.tags = ["myimage:latest"]  # <-- tags, not name
    mock_client.images.list.return_value = [mock_image]
    mock_from_env.return_value = mock_client

    docker_client = DockerClient()
    images = docker_client.list_images()

    assert len(images) == 1
    print(images[0])

    assert images[0].id == "12345"
    assert images[0].name == "myimage:latest"  # <-- test `tag`, not `name`


@patch('services.docker_client.docker.from_env')
def test_list_images_no_images(mock_from_env):
    mock_client = MagicMock()
    mock_client.images.list.return_value = []
    mock_from_env.return_value = mock_client

    docker_client = DockerClient()

    with pytest.raises(NoDataFoundException, match="No Docker images found."):
        docker_client.list_images()


@patch('services.docker_client.docker.from_env')
def test_list_containers_success(mock_from_env):
    mock_client = MagicMock()
    mock_container = MagicMock()
    mock_container.id = "abcde"
    mock_container.name = "my_container"
    mock_client.containers.list.return_value = [mock_container]
    mock_from_env.return_value = mock_client

    docker_client = DockerClient()
    containers = docker_client.list_containers()

    assert len(containers) == 1
    assert containers[0].id == "abcde"
    assert containers[0].name == "my_container"


@patch('services.docker_client.requests.get')
def test_get_latest_docker_version_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"tag_name": "v25.0.2"}
    mock_requests_get.return_value = mock_response

    docker_client = DockerClient()
    latest_version = docker_client.get_latest_docker_version()

    assert latest_version == "v25.0.2"


@patch('services.docker_client.docker.from_env')
def test_get_local_docker_version(mock_from_env):
    mock_client = MagicMock()
    mock_client.version.return_value = {"Version": "25.0.1"}
    mock_from_env.return_value = mock_client

    docker_client = DockerClient()
    local_version = docker_client.get_local_docker_version()

    assert local_version == "25.0.1"


@patch('services.docker_client.DockerClient.get_latest_docker_version')
@patch('services.docker_client.DockerClient.get_local_docker_version')
def test_is_installed_latest_version_true(mock_get_local, mock_get_latest):
    mock_get_local.return_value = "25.0.2"
    mock_get_latest.return_value = "25.0.2"

    docker_client = DockerClient()
    assert docker_client.is_installed_latest_version() is True


@patch('services.docker_client.DockerClient.get_latest_docker_version')
@patch('services.docker_client.DockerClient.get_local_docker_version')
def test_is_installed_latest_version_false(mock_get_local, mock_get_latest):
    mock_get_local.return_value = "25.0.1"
    mock_get_latest.return_value = "25.0.2"

    docker_client = DockerClient()
    assert docker_client.is_installed_latest_version() is False
