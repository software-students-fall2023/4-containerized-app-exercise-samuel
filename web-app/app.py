from flask import (
    Flask,
    render_template,
    request,
    redirect,
    abort,
    url_for,
    make_response,
    session,
)
import pymongo
from pymongo import MongoClient
import os
import dotenv
from dotenv import load_dotenv
from datetime import datetime
import sys
sys.path.append('../')
from database import db

#print(sys.path)


app = Flask(__name__)
app.secret_key = os.urandom(24)

if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


@app.route("/")
def hello(): 
    return render_template("victory.html")

@app.route("/victory", methods=["GET"])
def victory(): 
    return render_template("victory.html")

@app.route("/thumbsUp", methods=["GET"])
def thumbsUp(): 
    return render_template("thumbsUp.html")

@app.route("/thumbsDown", methods=["GET"])
def thumbsDown(): 
    return render_template("thumbsDown.html")

@app.route("/stop", methods=["GET"])
def stop(): 
    return render_template("stop.html")

@app.route("/rock", methods=["GET"])
def rock(): 
    return render_template("rock.html")

