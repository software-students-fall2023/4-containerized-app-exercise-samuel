'''
Face detection using OpenCV.
- using pre-trained classifiers available here: https://github.com/opencv/opencv/tree/master/data/haarcascades
- read more on this type of classifier here: https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html

'''

import cv2 as cv
from find_camera_devices import get_first_working_device_index

def run():
    """
        Run the FaceDetector and draw landmarks and boxes around detected faces
    """

    cap = cv.VideoCapture(get_first_working_device_index()) # get the first available camera device
    face_classifier = cv.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml') # load a pre-trained frontal view face classifier
    eye_classifier = cv.CascadeClassifier('classifiers/haarcascade_eye.xml') # load a pre-trained eye classifier
    smile_classifier = cv.CascadeClassifier('classifiers/haarcascade_smile.xml') # load a pre-trained smile classifier

    while True:
        success, frame = cap.read() # capture a camera frame

        if not success:
          # something went wrong this frame
          print("Skipping frame...")
          continue

        # our model only supports grayscale images, so convert the frame to grayscale
        frame_grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        face_coords = face_classifier.detectMultiScale(frame_grayscale, scaleFactor=1.3, minNeighbors=5) # detects faces and returns a list of coordinates for each face

        # iterate through each detected face and draw a rectangle around it
        for coords in face_coords:
          face_x, face_y, face_w, face_h = coords # destructure list of coordinates into separate variables
          color = (255, 0, 0) # red
          thickness = 5
          cv.rectangle(frame, (face_x, face_y), (face_x+face_w, face_y+face_h), color, thickness) # draw a rectangle around the face
          cv.putText(frame, 'Hello, face.', (face_x + 20, face_y + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5 , color)

          # crop just the face so we can look for eyes and smiles
          face_grayscale = frame_grayscale[face_y:face_y+face_h, face_x:face_x+face_w] # get just the face from the grayscale frame

          # detect eyes within the face
          eye_coords = eye_classifier.detectMultiScale(face_grayscale, scaleFactor=1.3, minNeighbors=5) # detect eyes in the face
          for coords in eye_coords:
            eye_x, eye_y, eye_w, eye_h = coords # coords within the cropped face
            color = (0, 255, 0) # green
            thickness = 3
            # draw an oval around the eye... convert face crop coords back to global coordinates
            cv.ellipse(frame, (face_x+eye_x+eye_w//2, face_y+eye_y+eye_h//2), (eye_w//2, eye_h//2), 0, 0, 360, color, thickness)
            cv.putText(frame, 'Hello, eye.', (face_x+eye_x + 10, face_y+eye_y+(eye_h//2)), cv.FONT_HERSHEY_SIMPLEX, 0.5 , color)

          # detect smiles within the face
          smile_coords = smile_classifier.detectMultiScale(face_grayscale, scaleFactor=1.3, minNeighbors=40) # detect smiles in the face
          for coords in smile_coords:
            smile_x, smile_y, smile_w, smile_h = coords # coords within the cropped face
            color = (0, 0, 255) # blue
            thickness = 3
            # draw a rectangle around the smile... convert face crop coords back to global coordinates
            cv.rectangle(frame, (face_x+smile_x, face_y+smile_y), (face_x+smile_x+smile_w, face_y+smile_y+smile_h), color, thickness)
            cv.putText(frame, 'Hello, smile.', (face_x+smile_x+20, face_y+smile_y+(smile_h//2)), cv.FONT_HERSHEY_SIMPLEX, 0.5 , color)


        # Show the frame
        cv.imshow('I see you!', frame)

        # Stop if escape key, 'x', or 'q' key is pressed
        key_code = cv.waitKey(25) & 0xFF # wait for 25ms and get any key code that was pressed
        escape_key_code = 27
        if key_code in [ord('q'), ord('x'), escape_key_code]:
            break

    # do cleanup to release the camera and other resources
    cap.release()
    cv.destroyAllWindows()
        
        
# Run the app
if __name__ == "__main__":
  run()
