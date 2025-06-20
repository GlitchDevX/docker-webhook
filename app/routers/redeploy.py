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
    image = daemon.images.pull(image_name, data.newTag)
    
    new_container = daemon.containers.run(image, detach=True,
        ports=prev_container.ports)

    if (data.healthCheck):
        await sleep(data.healthcheckTimeout)
    
        if (new_container.status == "exited"):
            prev_container.start()
            new_container.remove()
            return
    
    prev_container.remove()
        

@router.post("/image")
async def redeploy_image():
    pass