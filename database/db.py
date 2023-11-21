import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import dotenv
from dotenv import load_dotenv
import certifi


# load credentials and configuration options from .env file
load_dotenv()

db = None

client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client[os.getenv("MONGO_DBNAME")]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def users():
    return db.users.find_one({"name":"Lemon"})


#db.users.insert_one({"name":"Lemon"})