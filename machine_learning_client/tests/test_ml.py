"""
Testing machine learning 
"""
# pylint: disable=C0411
# pylint: disable=C0413
import sys
import os 
import pymongo
import pytest
from pymongo import MongoClient
from machine_learning_client import setup
sys.path.append("..")
from unittest.mock import patch, Mock, MagicMock
from pytest_mock_resources import create_mongo_fixture


def test_initialize_database_timeout_error():
    invalid_uri = "mongodb://invalid_uri"
    client = MongoClient(invalid_uri)
    database_name = "test_db"
    db_connection = setup.initialize_database(client, database_name)
    assert db_connection is None

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


