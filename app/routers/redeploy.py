from asyncio import sleep
import docker
from fastapi import APIRouter

from app.dto.requests.redeploy_container_data import RedeployContainerData


router = APIRouter(prefix="/redeploy")

@router.post("/container")
async def redeploy_container(data: RedeployContainerData):
    daemon = docker.from_env()

    prev_container = daemon.containers.get(data.containerId)
    prev_container.stop()

    image_name = prev_container.image.tags[0].split(":")[0] # split tag and get new image
    tag = f"{image_name}:{data.newTag}"
    image = daemon.images.pull(image_name, data.newTag)
    
    # new_container = daemon.containers.run(image, detach=True) as Container

    if (data.healthCheck):
        await sleep(data.healthcheckTimeout)
    
        # new_container.


@router.post("/image")
async def redeploy_image():
    pass