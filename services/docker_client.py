import docker
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from models.docker_model import DockerContainer, DockerImage
from typing import Union


# Disable SSL warnings globally for urllib3
urllib3.disable_warnings(InsecureRequestWarning)


class DockerClient:
    def __init__(self):
        # Initialize the Docker client from environment variables (default configuration)
        self.client = docker.from_env()

    def list_images(self) -> list[DockerImage]:
        """
        List all Docker images.
        """
        try:
            images = [DockerImage(image.id, image.tags[0] if image.tags else "untagged")  # Use "untagged" if no tags are available
                      for image in self.client.images.list()]
            return images
        except Exception as e:
            print(f"An error occurred while listing images: {str(e)}")
            return []

    def list_containers(self) -> list[DockerContainer]:
        """
        List all Docker containers.
        """
        try:
            containers = [DockerContainer(container.id,
                                          container.name) for container in self.client.containers.list(all=True)]
            return containers

        except Exception as e:
            print(f"An error occurred while listing containers: {str(e)}")
            return []

    def start_container(self, container_name):
        """
        Start a specific container by name.
        """
        try:
            container = self.client.containers.get(container_name)
            container.start()
            print(f"Container {container_name} started.")
        except Exception as e:
            print(f"An error occurred while starting the container: {str(e)}")

    def stop_container(self, container_name):
        """
        Stop a specific container by name.
        """
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            print(f"Container {container_name} stopped.")
        except Exception as e:
            print(f"An error occurred while stopping the container: {str(e)}")
