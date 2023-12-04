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
import os
import cv2
import pymongo
import mediapipe as mp
import tensorflow as tf
import numpy as np
import certifi
from pymongo.mongo_client import MongoClient
from flask import Flask

app = Flask(__name__)



@app.route("/")
def hello():
    return "hello"


def initialize_database():
    client = pymongo.MongoClient("mongodb://mongodb:27017")
    print("CLIENT : ", client)
    db = client["database"]
    if db is None:
        print("db not connected")
    return db




# def initialize_database(client, database_name):
#     """
#     Initializes the database connection and returns the db connection object
#     """
#     try:
#         client.admin.command("ping")
#         db_connection = client[database_name]
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#         return db_connection
#     except pymongo.errors.ServerSelectionTimeoutError as timeout_error:
#         print(f"Server selection timeout error: {timeout_error}")
#     except pymongo.errors.ConnectionFailure as connection_failure:
#         print(f"MongoDB connection failure: {connection_failure}")
#     return None


def load_class_name():
    """
    Initializes the gesture names and returns the list of gesture names
    """
    with open(
        "machine_learning_client/mp_hand_gesture/gesture.names", "r", encoding="utf-8"
    ) as file:
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


def load_gesture_model(model_path="machine_learning_client/mp_hand_gesture"):
    """
    Loads the gesture model from the given path
    """
    return tf.keras.models.load_model(model_path)


def load_class_names(file_path="machine_learning_client/mp_hand_gesture/gesture.names"):
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

@app.route("/camera")
def run_ml():
    """
    Main function that runs the hand gesture recognition system
    """
    cap = cv2.VideoCapture(0)

    client = MongoClient(
        os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where()
    )
    db_connection = initialize_database()

    if db_connection is None:
        return

    mp_hands, hands, mp_draw = initialize_hand_tracking()
    model = load_gesture_model()
    class_names = load_class_names()

    while True:
        _, frame = cap.read()

        processed_frame = process_frame(
            frame, hands, mp_hands, mp_draw, model, class_names, db_connection
        )

        cv2.imshow("Output", processed_frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
