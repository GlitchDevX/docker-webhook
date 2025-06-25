from fastapi import HTTPException


def container_not_found(container_id: str):
    return HTTPException(404, f"Container with id '{container_id}' was not found")

def container_healthcheck_failed(logs: str):
    return HTTPException(400, f"Docker container healthcheck failed with logs:\n{logs}")