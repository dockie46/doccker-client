from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.docker_client import DockerClient
from models.docker_model import DockerContainer
from dependencies import get_docker_client
from models.exceptions import NoDataFoundException

router = APIRouter(
    prefix="/api/containers",      # Všechny cesty budou začínat /items
    tags=["containers"]        # Pro lepší přehled ve Swagger UI
)


@router.get("/", response_model=List[DockerContainer], status_code=status.HTTP_200_OK)
def read_items(client: DockerClient = Depends(get_docker_client)):
    try:
        return client.list_containers()
    except NoDataFoundException as e:
        print("Actually, no Docker containers found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        print(
            f"An unexpected error occurred while listing containers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@router.post("/{container_id}/start", status_code=status.HTTP_201_CREATED)
def start(container_id: str, client: DockerClient = Depends(get_docker_client)):
    try:
        client.start_container(container_id)
        return {"message": f"Container '{container_id}' started successfully."}

    except NoDataFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e


@router.post("/{container_id}/stop", status_code=201)
def stop(container_id: str, client: DockerClient = Depends(get_docker_client)):
    try:
        client.stop_container(container_id)
        return {"message": f"Container '{container_id}' stoped successfully."}
    except NoDataFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
