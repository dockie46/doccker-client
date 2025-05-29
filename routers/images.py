from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.docker_client import DockerClient
from models.docker_model import DockerImage
from dependencies import get_docker_client
from models.exceptions import NoDataFoundException

router = APIRouter(
    prefix="/api/images",      # Všechny cesty budou začínat /items
    tags=["images"]        # Pro lepší přehled ve Swagger UI
)


@router.get("/", response_model=List[DockerImage], status_code=status.HTTP_200_OK)
def read_items(client: DockerClient = Depends(get_docker_client)):
    try:
        return client.list_images()
    except NoDataFoundException as e:
        print("Actually, no Docker images found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        print(
            f"An unexpected error occurred while listing images: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@router.get("/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
