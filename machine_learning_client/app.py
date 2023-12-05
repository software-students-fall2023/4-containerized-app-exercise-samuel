"""
Gesture Recognition System
"""
# pylint: disable=no-member
# pylint: disable=R1714
# pylint: disable=R0916
# pylint: disable=W0718
# pylint: disable=E0401
# pylint: disable=W0621
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=R1710
# pylint: disable C0303
# pylint: disable 103


import base64
import os
import cv2
import pymongo
import mediapipe as mp
import tensorflow as tf
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True

@app.route("/")
def hello():
    """
    Index page
    """
    return "hello"

def initialize_database():
    """
    Initialize a db
    """
    client = pymongo.MongoClient("mongodb://mongodb:27017")
    print("CLIENT:", client)
    db = client["database"]
    if db is None:
        print("db not connected")
    return db

def load_class_name():
    """
    Initializes the gesture names and returns the list of gesture names
    """
    with open("./mp_hand_gesture/gesture.names", "r", encoding="utf-8") as file:
        class_names = file.read().split("\n")
    return class_names

def initialize_hand_tracking():
    """
    Initializes the hand tracking model and returns the model and the drawing utility
    """
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.98)
    mp_draw = mp.solutions.drawing_utils
    return mp_hands, hands, mp_draw

def load_gesture_model(model_path="./mp_hand_gesture"):
    """
    Loads the gesture model from the given path
    """
    return tf.keras.models.load_model(model_path)

def load_class_names(file_path="./mp_hand_gesture/gesture.names"):
    """
    Loads the class names from the given file path
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().split("\n")

def process_frame(frame, hands, mp_hands, mp_draw, model, class_names, db_connection):
    """
    Processes the frame and returns the frame with the gesture label
    """
    x, y, _ = frame.shape
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    class_name = ""

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)

        prediction = model.predict([landmarks])
        class_id = np.argmax(prediction)
        class_name = class_names[class_id]
        print(class_name)

    cv2.putText(
        frame,
        class_name,
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (128, 0, 128),
        2,
        cv2.LINE_AA,
    )

    if class_name and class_name in (
        "peace",
        "fist",
        "stop",
        "rock",
        "thumbs up",
        "thumbs down",
    ):
        if db_connection is not None:
            db_connection.gestures.insert_one({"gesture": class_name})
            print("Inserted gesture into the database")

    return frame

# Declare global variables
MP_HANDS = None
HANDS = None
MP_DRAW = None
MODEL = None
CLASS_NAMES = None
DB_CONNECTION = None

DB_CONNECTION = initialize_database()
MP_HANDS, HANDS, MP_DRAW = initialize_hand_tracking()
MODEL = load_gesture_model()
CLASS_NAMES = load_class_names()

def decode_image_from_json(json_data):
    """
    Decode image
    """
    try:
        data = json_data
        if not data or "image" not in data:
            return "No image data", 400
        image_data = data["image"]
        encoded_data = image_data.split(",")[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

def generate_frames_from_json(frame, hands, mp_hands, mp_draw, model, class_names, db_connection):
    """
    Generate frames
    """
    processed_frame = process_frame(frame, hands, mp_hands,
    mp_draw, model, class_names, db_connection)
    if processed_frame is None:
        return None
    _, buffer = cv2.imencode('.jpg', processed_frame)
    frame_bytes = buffer.tobytes()
    return frame_bytes


@app.route("/test", methods=["POST"])
def test():
    """
    Testing route for gesture recognition
    """
    try:
        json_data = request.get_json()
        if json_data and "image" in json_data:
            frame = decode_image_from_json(json_data)
            if frame is None:
                return jsonify({"error": "Error decoding image"}), 500
            frame_bytes = generate_frames_from_json(frame, 
            HANDS, MP_HANDS, MP_DRAW, MODEL, CLASS_NAMES, DB_CONNECTION)
            if frame_bytes is None:
                return jsonify({"error": "Error processing image"}), 500
            processed_image_base64 = base64.b64encode(frame_bytes).decode("utf-8")
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Successfully processed image",
                        "processed_image": processed_image_base64,
                    }
                ),
                200,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=True)
