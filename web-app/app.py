from flask import Flask
import pymongo
from pymongo import MongoClient
import os
import dotenv
from dotenv import load_dotenv
from datetime import datetime
import sys
sys.path.append('../')
from database import db




print(sys.path)
app = Flask(__name__)
app.secret_key = os.urandom(24)

if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


@app.route("/")
def hello():
    user = db.users()
    
    return "hello" + user['name'] 




