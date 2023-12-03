"""
Front end web page routes
"""

# pylint: disable=R0911
# pylint: disable=W0718
# pylint: disable=W0621
# pylint: disable=W1510
# pylint: disable=E0401
# pylint: disable=R0801
import os
import sys
import subprocess
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, redirect, url_for


sys.path.append("../")


GESTURES_ARR = ["thumbs up", "thumbs down", "fist", "stop", "peace", "rock"]

app = Flask(__name__)
app.secret_key = os.urandom(24)


if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


def initialize_database():
    """
    Initializes the database connection and returns the db connection object
    """
    try:
        local_uri = "mongodb://mongodb:27017"
        client = MongoClient(local_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db_connection = client["database"]

        print("Connected to the DB")
        return db_connection
    except Exception as e:
        print(f"Error connecting to local MongoDB: {e}")
        return None

    # client = MongoClient(
    #     os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where()
    # )
    # try:
    #     client.admin.command("ping")
    #     db_connection = client[os.getenv("MONGO_DBNAME")]
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    #     return db_connection
    # except pymongo.errors.ServerSelectionTimeoutError as timeout_error:
    #     print(f"Server selection timeout error: {timeout_error}")
    # except pymongo.errors.ConnectionFailure as connection_failure:
    #     print(f"MongoDB connection failure: {connection_failure}")
    # return None


def gesture_display():
    """
    aggregate the frequency of each gesture
    find the gesture with the most frequency and return
    """
    db = initialize_database()

    if db is not None:
        thumb_up = db.gestures.count_documents({"gesture": "thumbs up"})
        thumb_down = db.gestures.count_documents({"gesture": "thumbs down"})
        fist = db.gestures.count_documents({"gesture": "fist"})
        open_palm = db.gestures.count_documents({"gesture": "stop"})
        peace = db.gestures.count_documents({"gesture": "peace"})
        love = db.gestures.count_documents({"gesture": "rock"})

        arr = [thumb_up, thumb_down, fist, open_palm, peace, love]

        max_obj = {"value": arr[0], "id": 0}
        for i in range(1, len(arr)):
            if arr[i] > max_obj["value"]:
                max_obj = {"value": arr[i], "id": i}

        print(
            "this is the thumb up gesture :"
            + str(thumb_up)
            + " thumb down: "
            + str(thumb_down)
            + "fist "
            + str(fist)
            + "stop "
            + str(open_palm)
            + "peace: "
            + str(peace)
            + "rock: "
            + str(love)
        )

        return GESTURES_ARR[max_obj["id"]]
    return redirect(url_for("hello"))


@app.route("/delete")
def delete():
    """
    delete gesture database
    """
    db = initialize_database()

    if db is not None and db.gestures is not None:
        db.gestures.delete_many({})

    return redirect(url_for("hello"))


@app.route("/test_db")
def test_db():
    db = initialize_database()
    collection = db["temp"]

    new_document = {
        "name": "Samuel Alexander Shally",
        "year": 2001,
        "city": "Kuala Lumpur",
    }

    result = collection.insert_one(new_document)

    inserted_id = result.inserted_id
    document = collection.find_one({"_id": inserted_id})

    if document:
        name = document.get("name", "Default Name")
        year = document.get("year", "Default Year")
        city = document.get("city", "Default City")
        data = f"My name is {name}, I was born in {year}, and I live in {city}."
    else:
        data = "Nothing in DB"

    return render_template("displayData.html", data=data)


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
    trigger the machine learning client and camera
    """
    try:
        file_path = "../machine_learning_client/setup.py"
        print(file_path)
        subprocess.run(["python", file_path])
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
    Pull the picture of churchill on victory gesture
    """
    return render_template("victory.html")


@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    """
    Pulls the picture of jesus on thumbs up gesture
    """
    return render_template("thumbsUp.html")


@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    """
    Pulls a picture of the devil on thumbs down gesture
    """
    return render_template("thumbsDown.html")


@app.route("/stop", methods=["GET"])
def stop():
    """
    Pull a picture of a snail on open palm gesture
    """
    return render_template("stop.html")


@app.route("/rock", methods=["GET"])
def rock():
    """
    Pulls a picture of a rock on closed fist gesture
    """
    return render_template("rock.html")
