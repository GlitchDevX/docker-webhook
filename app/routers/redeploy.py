from fastapi import APIRouter, HTTPException

from app.dto.requests.redeploy_container_data import RedeployContainerData
from app.services.redeploy import redeploy_container


router = APIRouter(prefix="/redeploy", tags=["Redeployment"])

@router.post("/container")
async def redeploy_container_route(data: RedeployContainerData):
    """
    Redeploys a given container by pulling a newer version of the containers image.
    Then stops the given container and starts a new container with the new image.
    \n\n
    The id of the newly created container will be returned."""
    return redeploy_container(data)

@router.post("/image")
async def redeploy_image_route():
    """
    Redeploys every container that uses the image provided by pulling the given version of the image.
    Then stops the containers and starts new containers with the new image.
    \n\n
    The id of the newly created containers will be returned.
    """
    raise HTTPException(501, "Endpoint not implemented yet")