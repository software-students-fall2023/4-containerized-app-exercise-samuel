"""
Testing machine learning 
"""
# pylint: disable=C0411
# pylint: disable=C0413
import sys
from pymongo import MongoClient
import numpy as np
import pytest
import json
from machine_learning_client import app

sys.path.append("..")
from unittest.mock import patch, Mock


@pytest.fixture
def mock_hands():
    return Mock()


@pytest.fixture
def mock_mp_hands():
    return Mock()


@pytest.fixture
def mock_mp_draw():
    return Mock()


@pytest.fixture
def mock_model():
    return Mock()


@pytest.fixture
def mock_db_connection():
    return Mock()

@pytest.fixture
def mock_load_model(monkeypatch):
    mock = Mock()
    monkeypatch.setattr("tensorflow.keras.models.load_model", mock)
    return mock

@pytest.fixture
def client():
    """
    Creates a flask testing client to simmulate calls to the web-app.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_hello_route(client):
    """
    Testing the returned status code of the default route.
    """
    response = client.app.get('/')
    assert response.status_code == 200

def test_post_request_without_input(client):
        response = client.app.post('/test', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 500

def test_load_class_name():
    """
    Test the returned class names from the load_class_name function
    """
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "gesture1\ngesture2"
        )
        class_names = app.load_class_name()
        assert class_names == ["gesture1", "gesture2"]


def test_initialize_hand_tracking():
    """
    Test the returned hand tracking model and drawing
    utility from the initialize_hand_tracking function
    """
    mp_hands, hands, mp_draw = app.initialize_hand_tracking()
    assert mp_hands is not None
    assert hands is not None
    assert mp_draw is not None


def test_load_gesture_model_success(mock_load_model):
    """
    Test the returned gesture model from the load_gesture_model function
    """
    expected_model = Mock()
    mock_load_model.return_value = expected_model
    result = app.load_gesture_model("mock_path")
    assert result == expected_model
    mock_load_model.assert_called_once_with("mock_path")


def test_process_frame_with_landmarks(
    mock_hands, mock_mp_hands, mock_mp_draw, mock_model, mock_db_connection
):
    """
    Test the returned frame from the process_frame function
    """
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    class_names = ["peace", "fist", "stop", "rock", "thumbs up", "thumbs down"]
    mock_result = Mock()
    mock_result.multi_hand_landmarks = [Mock()]
    mock_result.multi_hand_landmarks[0].landmark = [
        Mock(x=0.1, y=0.2),
        Mock(x=0.3, y=0.4),
    ]
    mock_hands.process.return_value = mock_result
    mock_model.predict.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]])
    result_frame = app.process_frame(
        frame,
        mock_hands,
        mock_mp_hands,
        mock_mp_draw,
        mock_model,
        class_names,
        mock_db_connection,
    )
    assert mock_hands.process.called_once_with(np.flip(frame, 1))
    assert mock_mp_draw.draw_landmarks.called_once_with(
        frame, mock_result.multi_hand_landmarks[0], mock_mp_hands.HAND_CONNECTIONS
    )
    assert mock_model.predict.called_once_with([[[10, 20], [30, 40]]])
    assert result_frame is not None


