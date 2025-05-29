# dependencies.py
from services.docker_client import DockerClient
from services.prediction_manager import ContainerMemoryManager


def get_docker_client():
    """
    Dependency that provides a Docker client instance.
    This function can be used with FastAPI's Depends to inject the Docker client
    into route handlers.
    """
    return DockerClient()


def get_prediction_manager():
    """
    Dependency that provides an instance of the prediction manager.
    This function can be used with FastAPI's Depends to inject the prediction manager
    into route handlers.
    """
    return ContainerMemoryManager()
