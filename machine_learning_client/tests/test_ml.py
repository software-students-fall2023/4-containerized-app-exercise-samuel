import cv2
import numpy as np
import pytest
import certifi
import os
import unittest 
import mediapipe as mp
import sys
from unittest.mock import MagicMock, patch

sys.path.append("..")
import machine_learning_client.setup
from machine_learning_client import setup

class TestProcessFrame(unittest.TestCase):
     
    def setUp(self):
        # Create a mock frame for testing
        self.mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Create mock objects for dependencies
        self.hands_mock = MagicMock()
        self.mp_hands_mock = MagicMock()
        self.mp_draw_mock = MagicMock()
        self.model_mock = MagicMock()
        self.class_names_mock = [
            "peace",
            "fist",
            "stop",
            "rock",
            "thumbs up",
            "thumbs down",
        ]
        self.db_connection_mock = MagicMock()



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
        Test the returned hand tracking model and drawing utility from the initialize_hand_tracking function
        """
        mp_hands, hands, mp_draw = setup.initialize_hand_tracking()
        assert mp_hands is not None
        assert hands is not None
        assert mp_draw is not None


    if __name__ == "__main__":
        test_load_class_name()
