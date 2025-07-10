import docker

from src.docker_webhook.app.common.exceptions import container_not_found

def try_get_container(daemon: docker.DockerClient, container_id: str):
    try:
        return daemon.containers.get(container_id)
    except:
        raise container_not_found(container_id)
    
def split_tag(tag: str):
    if ':' in tag:
        return tag.split(':')
    return [tag, None]
