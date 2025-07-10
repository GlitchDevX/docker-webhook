from fastapi import HTTPException


def container_not_found(container_id: str):
    return HTTPException(404, f"Container with id '{container_id}' was not found")

def container_healthcheck_failed(logs: str):
    return HTTPException(400, f"Docker container healthcheck failed with logs:\n{logs}")

def no_container_with_img_found(img_name: str):
    return HTTPException(404, f"Container with image name '{img_name}' was not found")

def container_healthchecks_failed(failed: int, total: int, logs: str):
    return HTTPException(400, f"{failed} of {total} containers healthcheck failed with logs:\n{logs}")