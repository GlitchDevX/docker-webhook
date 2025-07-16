import docker
from docker.models.containers import Container
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from docker_webhook.app.services.containers import get_container_logs, get_container_stats, get_containers


router = APIRouter(prefix="/container", tags=["Container Information"])

@router.get("/active")
async def active_containers():
    """
    Returns a list of all active docker containers.
    """
    return get_containers(False)

@router.get("/all")
async def all_containers():
    """
    Returns all docker container including paused and exited ones.
    """
    return get_containers(True)

@router.get("/stats")
async def stats(containerId: str):
    """
    Returns statistics of the container with the given containerId.
    """
    return get_container_stats(containerId)

@router.get("/logs")
async def logs(containerId: str):
    """
    Starts a log stream of the container with the given containerId.
    """
    return get_container_logs(containerId, False)

@router.get("/log-stream")
async def log_stream(containerId: str):
    """
    Starts a log stream of the container with the given containerId.
    """
    return get_container_logs(containerId, True)


