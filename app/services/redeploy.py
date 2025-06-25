from asyncio import sleep
import docker
from app.dto.requests.redeploy_container_data import RedeployContainerData
from app.common.container_utils import try_get_container
from app.common.exceptions import container_healthcheck_failed, container_not_found


async def redeploy_container(data: RedeployContainerData):
    daemon = docker.from_env()

    prev_container = try_get_container(daemon, data.containerId)
    if prev_container.image is None:
        raise container_not_found(data.containerId)

    image_name = prev_container.image.tags[0].split(":")[0] # split tag and get new image
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
