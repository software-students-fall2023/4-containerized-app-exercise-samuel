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
import requests
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, redirect, url_for, request, jsonify
import sys
from flask_cors import CORS
import numpy as np
import cv2
from io import BytesIO
import base64


sys.path.append("../")


GESTURES_ARR = ["thumbs up", "thumbs down", "fist", "stop", "peace", "rock"]

app = Flask(__name__)
CORS(app) 

app.secret_key = os.urandom(24)


if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


def initialize_database():
    """
    Initializes the database connection and returns the db connection object
    """
    try:
        local_uri = "mongodb://localhost:27017"
        client = MongoClient(local_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db_connection = client["database"]
        print("Connected to the DB")
        return db_connection
    except Exception as e:
        print(f"Error connecting to local MongoDB: {e}")
        return None


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


@app.route('/camera')
def camera():
    try:
        return render_template("video.html")
    except requests.RequestException as e:
        app.logger.error(f"An error occurred: {str(e)}")
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

from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from cvzone.HandTrackingModule import HandDetector  # Assuming this module is available in your environment

@app.route("/rep", methods=["POST"])
def rep():

    print("got here")
    try:
        data = request.json
        if not data or "frame" not in data:
            print("no data")
            return "No frame data", 400
        
        frame_data = data["frame"]
        encoded_data = frame_data.split(",")[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("Image processing done")

        # Example: Call the hand gesture function
        gesture = get_hand_gesture(img)
        
        return jsonify(success=True, gesture=gesture)  # Sending a success response back to the frontend with gesture information
    except Exception as e:
        print(f"Error decoding image: {e}")
        return jsonify(error=str(e)), 500  # Sending an error response back to the frontend

def get_hand_gesture(image):
    # Initialize HandDetector
    print("INSIDE HAND GESTURE FUNCTION")
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # Process the image and get hand information
    hands, _ = detector.findHands(image)

    # Check for hand gestures
    if hands:
        # Access landmarks
        landmarks = hands[0]['lmList']

        # Calculate scores for each gesture

        # Peace: If the index and middle fingers are extended and other fingers are closed
        peace_score = int(landmarks[8][1] < landmarks[5][1] and landmarks[12][1] < landmarks[9][1])

        # Thumbs Up: If the thumb is extended and other fingers are closed
        thumbs_up_score = int(landmarks[4][1] < landmarks[3][1] < landmarks[2][1] < landmarks[1][1])

        # Thumbs Down: If the thumb is extended and the rest are closed
        thumbs_down_score = int(landmarks[4][1] > landmarks[3][1] > landmarks[2][1] > landmarks[1][1])

        # Calculate total scores for each gesture
        total_scores = {
            "Peace": peace_score,
            "Thumbs Up": thumbs_up_score,
            "Thumbs Down": thumbs_down_score,
        }

        # Get the gesture with the highest score
        detected_gesture = max(total_scores, key=total_scores.get)

        # Print scores for debugging
        print("Scores:", total_scores)

        # Return the detected gesture
        if total_scores[detected_gesture] > 0:
            print(detected_gesture)
            return detected_gesture

    # No hand gestures detected
    print("NO GESTURE")
    return "No Gesture"


@app.route("/temp")
def temp():
    """
    the main page of the web app
    """
    return render_template("video.html")