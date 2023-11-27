"""
Does a thing. 
"""

import os
import sys
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)
sys.path.append('../')
import pymongo
from pymongo import MongoClient
import dotenv
from dotenv import load_dotenv
from datetime import datetime
import certifi
import subprocess


GESTURES_ARR = ["thumbs up","thumbs down","fist","stop","peace","rock"]

app = Flask(__name__)
app.secret_key = os.urandom(24)



if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


#create a db instance 
db = None

client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client[os.getenv("MONGO_DBNAME")]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def gesture_display():

    thumb_up = db.gestures.count_documents({"gesture":"thumbs up"})
    thumb_down = db.gestures.count_documents({"gesture":"thumbs down"})
    fist = db.gestures.count_documents({"gesture":"fist"})
    stop = db.gestures.count_documents({"gesture":"stop"})
    peace = db.gestures.count_documents({"gesture":"peace"})
    rock = db.gestures.count_documents({"gesture":"rock"})

    arr = [thumb_up,thumb_down,fist,stop,peace,rock]

    max_obj = {"value":arr[0],"id":0}
    for i in range(1,len(arr)):
        if(arr[i] > max_obj["value"]):
            max_obj = {"value":arr[i], "id":i}
    
    print(max_obj["id"])
    print(max_obj["value"])
    


    print("this is the thumb up gesture :"  + str(thumb_up) + " thumb down: " + str(thumb_down)  + "fist " + str(fist) + "stop " + str(stop) + "peace: " + str(peace) + "rock: " + str(rock))

    return GESTURES_ARR[max_obj["id"]]

@app.route("/delete")
def delete():
    db.gestures.drop()
    return redirect(url_for("hello"))

@app.route("/test")
def test():
  
    gest = gesture_display()
    print("Name: ", gest)
    if(gest == "stop"):
        return redirect(url_for("stop"))
    if(gest == "thumbs up"):
        return redirect(url_for("thumbs_up"))
    if(gest == "thumbs down"):
        return redirect(url_for("thumbs_down"))
    if(gest == "fist"):
        return redirect(url_for("rock"))
    if(gest == "peace"):
        return redirect(url_for("victory"))
    if(gest == "rock"):
        return redirect(url_for("victory"))

    return redirect(url_for("hello"))

@app.route("/camera")
def camera():
    try:
        file_path = 'machine_learning_client/setup.py'
        print(file_path)
        subprocess.run(['python', file_path])
        return "script success"
       
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/")
def hello():
    """
    Does a thing.
    """
    return render_template("welcome.html")


@app.route("/victory", methods=["GET"])
def victory():
    """
    Does a thing.
    """
    return render_template("victory.html")


@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    """
    Does a thing.
    """
    return render_template("thumbsUp.html")


@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    """
    Does a thing.
    """
    return render_template("thumbsDown.html")


@app.route("/stop", methods=["GET"])
def stop():
    """
    Does a thing.
    """
    return render_template("stop.html")


@app.route("/rock", methods=["GET"])
def rock():
    """
    Does a thing.
    """
    return render_template("rock.html")
