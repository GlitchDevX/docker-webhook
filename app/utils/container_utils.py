import docker
from fastapi import HTTPException

def try_get_container(daemon: docker.DockerClient, container_id: str):
    try:
        return daemon.containers.get(container_id)
    except:
        raise HTTPException(404, "Container with id '{container_id}' was not found")