from typing import Union
from urllib3.exceptions import InsecureRequestWarning
import requests
import urllib3
import docker
import docker.errors
from models.exceptions import NoDataFoundException
from models.docker_model import DockerContainer, DockerImage
from urllib3.exceptions import InsecureRequestWarning


# Disable SSL warnings globally for urllib3
urllib3.disable_warnings(InsecureRequestWarning)

class DockerClient:
    def __init__(self):
        try:
            self.client = docker.from_env()
            # Try pinging the Docker server
            self.client.ping()
        except docker.errors.DockerException as e:
            print(f"[DockerClient] Docker is not available: {e}")
            self.client = None

    def is_docker_online(self) -> bool:
        """
        Check if the Docker client is online.
        """
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except docker.errors.DockerException:
            return False

    def list_images(self) -> list[DockerImage]:
        """
        List all Docker images.
        """
        if not self.client:
            print("Docker client not initialized or Docker is offline.")
            return []

        try:
            images = [DockerImage(id=str(image.id), name=(image.tags[0] if image.tags else "untagged"))  # Use "untagged" if no tags are available
                      for image in self.client.images.list(all=True)]
            if not images:
                raise NoDataFoundException("No Docker images found.")

            return images
        except NoDataFoundException as e:
            raise e
        except Exception as e:
            print(f"An error occurred while listing images: {str(e)}")
            return []

    def list_containers(self) -> list[DockerContainer]:
        """
        List all Docker containers.
        """
        if not self.client:
            print("Docker client not initialized or Docker is offline.")
            return []

        try:
            containers = [
                DockerContainer(id=container.id, name=container.name)
                for container in self.client.containers.list(all=True)
            ]
            if not containers:
                raise NoDataFoundException("No Docker containers found.")
            return containers
        except Exception as e:
            print(f"An error occurred while listing containers: {str(e)}")
            return []

    def start_container(self, container_name):
        """
        Start a specific container by name.
        """
        if not self.client:
            print("Docker client not initialized or Docker is offline.")
            return

        try:
            container = self.client.containers.get(container_name)
            if container is None:
                raise NoDataFoundException(
                    f"Container {container_name} not found.")

            container.start()
            print(f"Container {container_name} started.")
        except docker.errors.NotFound as e:
            raise NoDataFoundException(
                f"Container '{container_name}' not found.") from e
        except Exception as e:
            print(f"An error occurred while starting the container: {str(e)}")
            raise e

    def stop_container(self, container_name):
        """
        Stop a specific container by name.
        """
        if not self.client:
            print("Docker client not initialized or Docker is offline.")
            return

        try:
            container = self.client.containers.get(container_name)
            container.stop()
            print(f"Container {container_name} stopped.")
        except NoDataFoundException as e:
            raise e
        except Exception as e:
            print(f"An error occurred while stopping the container: {str(e)}")
            raise e

    def get_latest_docker_version(self) -> Union[str, None]:
        """
        Fetch the latest Docker version from GitHub releases.
        """
        url = "https://api.github.com/repos/docker/docker-ce/releases/latest"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('tag_name')
        except requests.RequestException as e:
            print(f"Failed to get latest version: {e}")
            return None

    def get_local_docker_version(self) -> str:
        """
        Returns the version of the local Docker Engine.
        """
        client = docker.from_env()
        version_info = client.version()
        return version_info.get('Version', 'Unknown')

    def is_installed_latest_version(self) -> bool:
        """
        Check if the installed Docker version is the latest.
        """
        latest_version = self.get_latest_docker_version()
        if latest_version is None:
            return False

        installed_version = self.get_local_docker_version()
        return installed_version == latest_version
