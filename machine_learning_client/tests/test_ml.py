"""
Testing machine learning 
"""
# pylint: disable=C0411
# pylint: disable=C0413
import sys
from machine_learning_client import setup

sys.path.append("..")
from unittest.mock import patch


def test_load_class_name():
    """
    Test the returned class names from the load_class_name function
    """
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "gesture1\ngesture2"
        )
        class_names = setup.load_class_name()
        assert class_names == ["gesture1", "gesture2"]


def test_initialize_hand_tracking():
    """
    Test the returned hand tracking model and drawing
    utility from the initialize_hand_tracking function
    """
    mp_hands, hands, mp_draw = setup.initialize_hand_tracking()
    assert mp_hands is not None
    assert hands is not None
    assert mp_draw is not None


def test_processing_frame():
    """
    Test the returned processed image from the processing_image function
    """
    processed_frame = setup.process_frame(None, None, None, None, None, None, None)
    assert processed_frame is None
