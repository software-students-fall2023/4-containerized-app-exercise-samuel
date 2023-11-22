import mediapipe as mp
import time 
import cv2 

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

images = []
results = []
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if(result == None):
        return
    gesture = result.gestures
    print(gesture)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='machine-learning-client/gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with GestureRecognizer.create_from_options(options) as recognizer:

    print('gesture recognizer initialized')
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # Create a loop to read the latest frame from the camera using VideoCapture.read()
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        recognizer.recognize_async(mp_image, round(time.time() * 1000))

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
