import sys
import urllib3
from docker.errors import DockerException
from services.docker_client import DockerClient
from urllib3.exceptions import InsecureRequestWarning
from models.exceptions import NoDataFoundException

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

try:
    images = client.list_images()
    for image in images:
        print(image)
except NoDataFoundException as e:
    print("Actually, no Docker images found.")
except Exception as e:
    print(f"An unexpected error occurred while listing images: {str(e)}")

try:
    containers = client.list_containers()
    for container in containers:
        print(container)
except NoDataFoundException as e:
    print("Actually, no Docker containers found.")
except Exception as e:
    print(f"An unexpected error occurred while listing containers: {str(e)}")

try:
    container_id = input("Enter the container ID to start: ")
    client.start_container(container_id)
except NoDataFoundException as e:
    print(f"Container '{container_id}' not found.")
except Exception as e:
    print(f"Failed to start container '{container_id}': {str(e)}")

try:
    is_installed_latest_version = client.is_installed_latest_version()
    print(f"Is installed latest version: {is_installed_latest_version}")
except Exception as e:
    print(f"Occured with is installed latest '{container_id}': {str(e)}")
