import docker
from docker.models.containers import Container
from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/container", tags=["Container Information"])

@router.get("/active")
async def active_containers():
    daemon = docker.from_env()

    containers = daemon.containers.list()
    return list(map(map_container, containers))

@router.get("/all")
async def all_containers():
    daemon = docker.from_env()
    containers = daemon.containers.list(True)
    return list(map(map_container, containers))

@router.get("/stats")
async def stats(containerId: str):
    daemon = docker.from_env()
    container = daemon.containers.get(containerId)
    return container.stats(stream=False)

@router.get("/logs")
async def logs(containerId: str):
    daemon = docker.from_env()
    container = daemon.containers.get(containerId)
    return StreamingResponse(container.logs(stream=True))

def map_container(container: Container):
    # required for containers with missing images
    try:
        tags = list(filter(lambda x: x is not None, map(lambda t: split_tag(t)[1], container.image.tags)))
        image = split_tag(container.image.tags[0])[0]

        return { 
            "name": container.name,
            "id": container.id,
            "image": image,
            "tags": tags,
            "status": container.status,
            "ports": container.ports,
        }
    except:
        return None

def split_tag(tag: str):
    if ':' in tag:
        return tag.split(':')
    return [tag, None]

