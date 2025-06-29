from asyncio import sleep
import docker
from docker.models.containers import Container
from fastapi.responses import JSONResponse
from app.dto.requests.redeploy_container_data import RedeployContainerData
from app.common.container_utils import split_tag, try_get_container
from app.common.exceptions import container_healthcheck_failed, container_healthchecks_failed, container_not_found, no_container_with_img_found
from app.dto.requests.redeploy_image_data import RedeployImageData


async def redeploy_container(data: RedeployContainerData):
    daemon = docker.from_env()

    prev_container = try_get_container(daemon, data.containerId)
    if prev_container.image is None:
        raise container_not_found(data.containerId)

    image_name = split_tag(prev_container.image.tags[0])[0] # split tag and get new image
    image = daemon.images.pull(image_name, data.newTag)
    
    prev_container.stop()

    new_container = daemon.containers.run(image, detach=True, ports=prev_container.ports, environment=data.environment)

    if (data.healthCheck):
        await sleep(data.healthcheckTimeout)
    
        if (new_container.status == "exited"):
            prev_container.start()
            logs = new_container.logs(stream=False).decode("utf-8")
            new_container.remove()
            raise container_healthcheck_failed(logs)
    
    prev_container.remove()
    return { "containerId": new_container.id }

async def redeploy_image(data: RedeployImageData):
    daemon = docker.from_env()

    all_containers: list[Container] = daemon.containers.list()
    containers: list[Container] = []
    for container in all_containers:
        if container.image is None:
            continue

        img_name = split_tag(container.image.tags[0])[0]
        if data.imageName == img_name:
            containers.append(container)
    
    if len(containers) == 0:
        if not data.allowNew:
            raise no_container_with_img_found(data.imageName)
        return _start_new_container(daemon, data.imageName, data.newTag, data.environment)
    
    full_tag = f"{data.imageName}:{data.newTag}"
    daemon.images.pull(full_tag)

    new_containers: list[Container] = []
    for container in containers:
        container.stop()
        new_container = daemon.containers.run(full_tag, detach=True, ports=container.ports, environment=data.environment)
        new_containers.append(new_container)

    healthchecks_failed = 0
    failed_logs = ""
    if data.healthCheck:
        await sleep(data.healthcheckTimeout)
        for container in new_containers:
            if container.status == "exited":
                healthchecks_failed += 1
                failed_logs += container.logs(stream=False).decode("utf-8") + "\n"
        
        if healthchecks_failed > 0:
            for index, container in enumerate(new_containers):
                containers[index].start()
                container.remove()
            raise container_healthchecks_failed(healthchecks_failed, len(containers), failed_logs)
    

    return { "containerIds": list(map(lambda c: c.id, new_containers)) }

def _start_new_container(daemon: docker.DockerClient, img_name: str, tag: str, env: list[str]):
    full_tag = f"{img_name}:{tag}"
    daemon.images.pull(full_tag)
    container = daemon.containers.run(full_tag, environment=env, detach=True)
    return JSONResponse({"containerId": container.id}, status_code=201)
