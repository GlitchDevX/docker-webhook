import subprocess
import docker
from docker.client import DockerClient

def redeploy_container(image: str):
    client = docker.from_env()

    print(client.containers.list(True))
    print(client.images.pull(image))

    stop_previous_container(client, image)
    
    start_new_container(client, image)
    
    stop_previous_container(client, image)

def stop_previous_container(client: DockerClient, image: str):
    pass

def start_new_container(client: DockerClient, image: str):
    pass

def restart_previous_container(client: DockerClient, image: str):
    pass
