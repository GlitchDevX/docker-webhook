from unittest.mock import MagicMock, Mock
import docker
from docker.errors import NotFound
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.services.containers import get_container_logs, get_container_stats, get_containers

mock_container = MagicMock()
mock_container.image.tags = ["test:1.12.4", "test:latest"]
mock_container.name = "someContainer"
mock_container.id = "someContainerId"
mock_container.status = "doomed"
mock_container.ports = "some:port"
mock_container.logs.return_value = b'Hello World!'
mock_container.stats.return_value = {"some": "stats"}

mapped_mock_container = [{'id': 'someContainerId', 'image': 'test', 'tags': ['1.12.4', 'latest'], 'name': 'someContainer', 'ports': 'some:port', 'status': 'doomed'}]

def test_get_containers():
    list_response_mock = MagicMock(return_value=[mock_container])

    list_func_mock = MagicMock()
    list_func_mock.list = list_response_mock

    container_attr_mock = MagicMock()
    container_attr_mock.containers = list_func_mock
    
    daemon_mock = MagicMock(return_value=container_attr_mock)
    docker.from_env = daemon_mock

    containers = get_containers(False)

    assert containers == mapped_mock_container

    docker.from_env.assert_called_once()
    list_response_mock.assert_called_once_with(False)

def test_get_containers_logs():
    get_func_mock = MagicMock()
    get_func_mock.get = MagicMock(return_value=mock_container)

    container_attr_mock = MagicMock()
    container_attr_mock.containers = get_func_mock
    
    daemon_mock = MagicMock(return_value=container_attr_mock)
    docker.from_env = daemon_mock

    logs = get_container_logs("someContainerId", False)

    assert logs == ["Hello World!"]

    docker.from_env.assert_called_once()
    get_func_mock.get.assert_called_once_with("someContainerId")

def test_get_containers_logstream():
    get_func_mock = MagicMock()
    get_func_mock.get = MagicMock(return_value=mock_container)

    container_attr_mock = MagicMock()
    container_attr_mock.containers = get_func_mock
    
    daemon_mock = MagicMock(return_value=container_attr_mock)
    docker.from_env = daemon_mock

    logs = get_container_logs("someContainerId", True)

    assert type(logs) == StreamingResponse

    docker.from_env.assert_called_once()
    get_func_mock.get.assert_called_once_with("someContainerId")

def test_throw_when_no_container_found_logs():
    get_func_mock = MagicMock()
    get_func_mock.get = Mock(side_effect=NotFound("haha"))

    container_attr_mock = MagicMock()
    container_attr_mock.containers = get_func_mock
    
    daemon_mock = MagicMock(return_value=container_attr_mock)
    docker.from_env = daemon_mock

    try:
        get_container_logs("someContainerId", False)
        assert False
    except HTTPException as err:
        assert err.status_code == 404
        assert err.detail == "Container with id 'someContainerId' was not found"
    except Exception as err:
        assert False

    docker.from_env.assert_called_once()
    get_func_mock.get.assert_called_once_with("someContainerId")

def test_get_containers_stats():
    get_func_mock = MagicMock()
    get_func_mock.get = MagicMock(return_value=mock_container)

    container_attr_mock = MagicMock()
    container_attr_mock.containers = get_func_mock
    
    daemon_mock = MagicMock(return_value=container_attr_mock)
    docker.from_env = daemon_mock

    stats = get_container_stats("someContainerId")

    assert stats == {"some": "stats"}

    docker.from_env.assert_called_once()
    get_func_mock.get.assert_called_once_with("someContainerId")