"""
web app file
"""
import os
import sys
import subprocess
from pymongo import MongoClient
import certifi
from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)
sys.path.append('../')

# pylint: disable=R0911
# pylint: disable=W0718
# pylint: disable=W0621
# pylint: disable=W1510
# pylint: disable=E0401
# pylint: disable=R0801


GESTURES_ARR = ["thumbs up","thumbs down","fist","stop","peace","rock"]

app = Flask(__name__)
app.secret_key = os.urandom(24)



if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


#create a db instance
DB = None

client = MongoClient(os.getenv('MONGO_URI'),
serverSelectionTimeoutMS=5000,tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    DB = client[os.getenv("MONGO_DBNAME")]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def gesture_display():
    """
    aggregate the frequency of each gesture
    find the gesture with the most frequency and return
    """
    thumb_up = DB.gestures.count_documents({"gesture":"thumbs up"})
    thumb_down = DB.gestures.count_documents({"gesture":"thumbs down"})
    fist = DB.gestures.count_documents({"gesture":"fist"})
    open_palm = DB.gestures.count_documents({"gesture":"stop"})
    peace = DB.gestures.count_documents({"gesture":"peace"})
    love = DB.gestures.count_documents({"gesture":"rock"})

    arr = [thumb_up,thumb_down,fist,open_palm,peace,love]

    max_obj = {"value":arr[0],"id":0}
    for i in range(1,len(arr)):
        if arr[i] > max_obj["value"]:
            max_obj = {"value":arr[i], "id":i}

    print("this is the thumb up gesture :"  + str(thumb_up) + " thumb down: "
          + str(thumb_down) + "fist "
        + str(fist) + "stop " + str(open_palm) + "peace: " + str(peace) + "rock: " + str(love))

    return GESTURES_ARR[max_obj["id"]]

@app.route("/delete")
def delete():
    """
    delete gesture database
    """
    DB.gestures.drop()
    return redirect(url_for("hello"))

@app.route("/test")
def test():
    """
    first get the gesture with the most frequency,
    then redirect user to the corresponding route
    """
    gest = gesture_display()
    print("Name: ", gest)
    if gest == "stop":
        return redirect(url_for("stop"))
    if gest == "thumbs up":
        return redirect(url_for("thumbs_up"))
    if gest == "thumbs down":
        return redirect(url_for("thumbs_down"))
    if gest == "fist":
        return redirect(url_for("rock"))
    if gest == "peace":
        return redirect(url_for("victory"))
    if gest == "rock":
        return redirect(url_for("victory"))

    return redirect(url_for("hello"))

@app.route("/camera")
def camera():
    """
    trigger the machine learning client
    """
    try:
        file_path = 'machine_learning_client/setup.py'
        print(file_path)
        subprocess.run(['python', file_path])
        return redirect(url_for("hello"))

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/")
def hello():
    """
    the main page of the web app
    """
    return render_template("welcome.html")


@app.route("/victory", methods=["GET"])
def victory():
    """
    takes the user to the victory page
    """
    return render_template("victory.html")


@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    """
   takes the user to the thumbs up page
    """
    return render_template("thumbsUp.html")


@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    """
    takes the user to the thumbs down page
    """
    return render_template("thumbsDown.html")


@app.route("/stop", methods=["GET"])
def stop():
    """
    takes the user to the stop page
    """
    return render_template("stop.html")


@app.route("/rock", methods=["GET"])
def rock():
    """
    takes the user to the rock page
    """
    return render_template("rock.html")
