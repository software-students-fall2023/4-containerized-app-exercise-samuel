"""
Hand Gesture Recognition Script
Adapted from: https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/

This is a Python script with ahand gesture recognition 
system using Python and OpenCV. 
The detection process used the MediaPipe library, 
while the recognition aspect utilized the TensorFlow framework.
"""
# pylint: disable=no-member
# pylint: disable=R1714
# pylint: disable=R0916
# pylint: disable=W0718
import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from pymongo.mongo_client import MongoClient
import certifi






# create a db instance
DB = None
client = MongoClient(os.getenv('MONGO_URI'),
    serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    DB = client[os.getenv("MONGO_DBNAME")]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.98)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = tf.keras.models.load_model("machine_learning_client/mp_hand_gesture")

# Load class names
with open(
    "machine_learning_client/mp_hand_gesture/gesture.names", "r", encoding="utf-8"
) as file:
    classNames = file.read().split("\n")

print(classNames)

# Initialize the webcam for Hand Gesture Recognition Python project
cap = cv2.VideoCapture(0)

while True:
    # Read each frame from the webcam
    _, frame = cap.read()
    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)

    CLASS_NAME = ""

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        # Show the final output
        # Predict gesture in Hand Gesture Recognition project
        prediction = model.predict([landmarks])
        # print(prediction)
        classID = np.argmax(prediction)
        CLASS_NAME = classNames[classID]

        print(CLASS_NAME)
        if CLASS_NAME and (CLASS_NAME == "peace" or CLASS_NAME == "fist" or CLASS_NAME == "stop"
                           or CLASS_NAME == "rock" or CLASS_NAME == "thumbs up"
                           or CLASS_NAME == "thumbs down"):
            DB.gestures.insert_one({"gesture":CLASS_NAME})

    # show the prediction on the frame
    cv2.putText(
        frame, CLASS_NAME, (10, 50), cv2.FONT_ITALIC, 1, (128, 0, 128), 2, cv2.LINE_AA
    )

    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
