"""
Testing machine learning 
"""
# pylint: disable=C0411
# pylint: disable=C0413
import sys

import numpy as np
import pytest
from machine_learning_client import app

sys.path.append("..")
from unittest.mock import patch, Mock


@pytest.fixture
def mock_hands():
    """
    mock hands
    """
    return Mock()


@pytest.fixture
def mock_mp_hands():
    """
    mock
    """
    return Mock()


@pytest.fixture
def mock_mp_draw():
    """
    mock
    """
    return Mock()


@pytest.fixture
def mock_model():
    """
    mock model
    """
    return Mock()


@pytest.fixture
def mock_db_connection():
    """
    mock db
    """
    return Mock()

@pytest.fixture
def mock_load_model(monkeypatch):
    """
    mock load model
    """
    mock = Mock()
    monkeypatch.setattr("tensorflow.keras.models.load_model", mock)
    return mock


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


def test_load_gesture_model_success(mock_load_model_param):
    """
    Test the returned gesture model from the load_gesture_model function
    """
    expected_model = Mock()
    mock_load_model_param.return_value = expected_model
    result = app.load_gesture_model("mock_path")
    assert result == expected_model
    mock_load_model_param.assert_called_once_with("mock_path")


def test_process_frame_with_landmarks(
    mock_hands_param, mock_mp_hands_param,
    mock_mp_draw_param, mock_model_param, mock_db_connection_param
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
    mock_hands_param.process.return_value = mock_result
    mock_model.predict.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]])
    result_frame = app.process_frame(
        frame,
        mock_hands_param,
        mock_mp_hands_param,
        mock_mp_draw_param,
        mock_model_param,
        class_names,
        mock_db_connection_param,
    )
    assert mock_hands_param.process.called_once_with(np.flip(frame, 1))
    assert mock_mp_draw_param.draw_landmarks.called_once_with(
        frame, mock_result.multi_hand_landmarks[0], mock_mp_hands_param.HAND_CONNECTIONS
    )
    assert mock_model_param.predict.called_once_with([[[10, 20], [30, 40]]])
    assert result_frame is not None
