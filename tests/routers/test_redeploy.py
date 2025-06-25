import docker
import pytest
from pytest_mock import MockerFixture

from app.dto.requests.redeploy_container_data import RedeployContainerData
from app.routers.redeploy import redeploy_container_route

def test_redeploy_container(mocker: MockerFixture):
    test_data = RedeployContainerData(containerId="testContainerId", newTag="someVersion", environment=["DB_PWD=SecurePassword"])
    
    daemon_mock = mocker.patch("docker.from_env")

    # daemon_mock.return_value.containers.run.return_value = { "id": "containerId" }
    
    redeploy_container_route(test_data)

    # daemon_mock.containers.run.assert_called_once()

    # docker.with_daemon.assert_called_once()