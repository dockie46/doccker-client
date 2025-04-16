import sys
import docker
import urllib3
from docker.errors import DockerException
from services.docker_client import DockerClient
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings globally for urllib3
urllib3.disable_warnings(InsecureRequestWarning)

try:
    client = DockerClient()
except DockerException as e:
    print("Docker is not running or cannot be reached. Please start Docker and try again.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while initializing DockerClient: {str(e)}")
    sys.exit(1)

images = client.list_images()
for image in images:
    print(image)

data = client.list_containers()
for container in data:
    print(container)

try:
    container_id = input("Enter the container ID to start: ")
    client.start_container(container_id)
except Exception as e:
    print(f"Failed to start container '{container_id}': {str(e)}")
