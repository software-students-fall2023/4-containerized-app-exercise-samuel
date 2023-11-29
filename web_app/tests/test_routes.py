"""
Tests to check the front end routes are working correctly.
"""
# pylint: disable=W0621
# pylint: disable=C0413
# pylint: disable=E0401

import sys
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
import pymongo
import os
import sys
import certifi


sys.path.append("..")

from app import app, initialize_database, gesture_display

# KEY - RUN WITH: python -m pytest


@pytest.fixture
def mocker():
    from unittest.mock import Mock
    return Mock()

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
    response = client.get("/")
    assert response.status_code == 200


def test_vicotory_route(client):
    """
    Test the retuned status code of the victory route.
    """
    response = client.get("/victory")
    assert response.status_code == 200


def test_thumbs_up_route(client):
    """
    Test the retuned status code of the thumbs_up route.
    """
    response = client.get("/thumbsUp")
    assert response.status_code == 200


def test_thumbs_down_route(client):
    """
    Test the retuned status code of the thumbs down route.
    """
    response = client.get("/thumbsDown")
    assert response.status_code == 200


def test_stop_route(client):
    """
    Test the retuned status code of the stop route.
    """
    response = client.get("/stop")
    assert response.status_code == 200


def test_rock_route(client):
    """
    Test the retuned status code of the rock route.
    """
    response = client.get("/rock")
    assert response.status_code == 200


def test_camera(client):
    """
    Test the camera route. The camera route redirects to the hello route
    """
    response = client.get("/camera")
    assert response.status_code == 302


def test_delete_route(client):
    """
    Test the delete route
    """
    response = client.get("/delete")
    assert response.status_code == 302


def test_test_route(client):
    """
    Test the test route
    """
    response = client.get("/test")
    assert response.status_code == 302


def test_initialize_database():
    """
    Test the initialize database function
    """
    with patch("pymongo.MongoClient") as mock_client:
        mock_db = MagicMock()
        mock_client.return_value = mock_db

        mock_db.admin.command.return_value = True

        db = initialize_database()

        # Print the calls made on the mock objects
        print(f"mock_client.call_args_list: {mock_client.call_args_list}")
        print(f"mock_db.admin.command.call_args_list: {mock_db.admin.command.call_args_list}")

        mock_db.admin.command.assert_called_with('Ping')

        assert db is mock_db


def test_initialize_database_failure():
    """
    Test the initialize_database function when it fails to connect
    """
    # Mock the MongoClient object
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_client.return_value = mock_db

        # Mock unsuccessful ping
        mock_db.admin.command.side_effect = pymongo.errors.ServerSelectionTimeoutError

        # Call the function
        db = initialize_database()

        # Check if function called the command method with 'ping'
        mock_db.admin.command.assert_called_with('ping')

        # Check if the function returns None
        assert db is None



