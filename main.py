import urllib3
from services.docker_client import DockerClient
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings globally for urllib3
urllib3.disable_warnings(InsecureRequestWarning)
client = DockerClient()

images = client.list_images()
for image in images:
    print(image)

data = client.list_containers()
for container in data:
    print(container)

container_id = input("Enter the container ID to start: ")

client.start_container(container_id)
# print(f"Container {container_id} started.")
