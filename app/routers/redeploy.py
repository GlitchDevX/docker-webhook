from asyncio import sleep
import docker
from docker.errors import NotFound
from fastapi import APIRouter, HTTPException

from app.dto.requests.redeploy_container_data import RedeployContainerData


router = APIRouter(prefix="/redeploy")

@router.post("/container")
async def redeploy_container(data: RedeployContainerData):
    daemon = docker.from_env()

    try:
        prev_container = daemon.containers.get(data.containerId)
    except NotFound:
        raise HTTPException(404, "Docker container not found")

    image_name = prev_container.image.tags[0].split(":")[0] # split tag and get new image
    image = daemon.images.pull(image_name, data.newTag)
    
    prev_container.stop()

    new_container = daemon.containers.run(image, detach=True, ports=prev_container.ports, environment=data.environment)

    if (data.healthCheck):
        await sleep(data.healthcheckTimeout)
    
        if (new_container.status == "exited"):
            prev_container.start()
            new_container.remove()
            return
    
    prev_container.remove()
    return { "containerId": new_container.id }
        

@router.post("/image")
async def redeploy_image():
    pass