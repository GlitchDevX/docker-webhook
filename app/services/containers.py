import docker
from docker.models.containers import Container
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.utils.container_utils import try_get_container

def get_containers(all: bool):
    daemon = docker.from_env()

    containers = daemon.containers.list(all)
    mapped_containers = map(map_container, containers)
    filtered_containers = filter(lambda x: x is not None, mapped_containers)

    return list(filtered_containers)

def get_container_stats(container_id: str):
    daemon = docker.from_env()

    container = try_get_container(daemon, container_id)
    return container.stats(stream=False)

def get_container_logs(container_id: str, stream: bool):
    daemon = docker.from_env()
    container = try_get_container(daemon, container_id)

    if stream:
        return StreamingResponse(container.logs(stream=True))
    else:
        logs = container.logs(stream=False)
        return str(logs).split("\\n")

def map_container(container: Container):
    if container.image is None:
        return None

    tags = list(filter(lambda x: x is not None, map(lambda t: split_tag(t)[1], container.image.tags)))
    image_name = split_tag(container.image.tags[0])[0]

    return { 
        "name": container.name,
        "id": container.id,
        "image": image_name,
        "tags": tags,
        "status": container.status,
        "ports": container.ports,
    }

def split_tag(tag: str):
    if ':' in tag:
        return tag.split(':')
    return [tag, None]
