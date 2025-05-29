import pytest
from unittest.mock import patch, MagicMock
from services.prediction_manager import ContainerMemoryManager
from models.docker_model import PredictionResult
from docker.errors import DockerException


@patch("services.prediction_manager.docker.from_env")
def test_fetch_container_stats(mock_from_env):
    mock_client = MagicMock()
    mock_container = MagicMock()
    mock_container.name = "test_container"
    mock_container.stats.return_value = {
        "memory_stats": {"usage": 104857600}  # 100 MB
    }

    mock_client.containers.list.return_value = [mock_container]
    mock_client.ping.return_value = True
    mock_from_env.return_value = mock_client

    manager = ContainerMemoryManager()
    manager.fetch_container_stats()

    assert not manager.df.empty
    assert "memory_usage" in manager.df.columns
    assert manager.df.iloc[0]["memory_usage"] == 100.0


@patch("services.prediction_manager.ContainerMemoryManager.fetch_container_stats")
def test_predict_memory_usage(mock_fetch_stats):
    manager = ContainerMemoryManager()

    # Fake DataFrame directly
    manager.df = manager.df = manager.df.from_dict({
        "name": ["container1", "container2"],
        "memory_usage": [100.0, 200.0]
    })

    result: PredictionResult = manager.predict_memory_usage()

    assert isinstance(result.predicted_next, float)
    assert result.predicted_next == 150.0  # mean of 100 and 200
    assert len(result.data) == 2
    assert "container1" in result.summary
    assert "🔮 Predicted memory usage" in result.summary


@patch("services.prediction_manager.docker.from_env")
def test_get_client_returns_valid_client(mock_from_env):
    mock_client = MagicMock()
    mock_from_env.return_value = mock_client

    manager = ContainerMemoryManager()
    client = manager.get_client()
    assert client is not None
    assert client == mock_client


@patch("services.prediction_manager.docker.from_env")
def test_get_client_handles_exception(mock_from_env):
    mock_from_env.side_effect = DockerException("Docker failure")

    manager = ContainerMemoryManager()
    assert manager.get_client() is None
