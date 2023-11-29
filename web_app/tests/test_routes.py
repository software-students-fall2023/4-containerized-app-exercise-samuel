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
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
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
    os.environ["MONGO_URI"] = os.getenv("MONGO_URI")
    os.environ["MONG0_DBNAME"] =  os.getenv("MONGO_DBNAME")

    print(f'Database name from env: {os.getenv("MONGO_DBNAME")}')

    db_connection = initialize_database()

    assert isinstance(db_connection, Database), "DB connection is not an instance of MongoClient"

    del os.environ["MONGO_URI"]
    del os.environ["MONGO_DBNAME"]

   
        
        

        



