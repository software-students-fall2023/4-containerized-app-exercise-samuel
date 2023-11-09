'''
Capture webcam video using opencv-python (i.e. cv2).
Install dependencies and run this file:
  pipenv install
  pipenv run python test_webcam.py
'''

import cv2
from find_camera_devices import get_first_working_device_index

def get_video_object():
  '''
  Returns a video object using the first working camera device.
  '''

  device_index = get_first_working_device_index() # get the first working camera device index

  try:
    video_object = cv2.VideoCapture(device_index) # create a video object
    return video_object
  except:
    # there was no working camera device
    print("No working camera device found!")
    return None
   
def main(): 
  video_object = get_video_object() # get a working video object
  if video_object is None:
    # abort, if no video object is available
    print("Quitting...")
    return

  # handling errors
  # if any erros is occured during the running of the program
  # then it handles
  try :
    # run a infinite loop to read the frames
    while(True):

      # read a video frame by frame
      # read() returns tuple in which 1st item is boolean value
      # either True or False and 2nd item is frame of the video.
      # read() returns False when live video is ended so
      # no frame is readed and error will be generated.
      ret,frame = video_object.read()
      
      # show the frame on the newly created image window
      cv2.imshow("I'm watching you!",frame)

      # this condition is used to run a frames at the interval of 10 mili sec
      # and if in b/w the frame running , any one want to stop the execution .
      if cv2.waitKey(10) & 0xFF == ord('q') :

        # break out of the while loop
        break

  except:
    # if error occur then this block of code is run
    print("Video has ended..")

  # release the video object, be nice.
  video_object.release()
  cv2.destroyAllWindows()

# if running this file directly...
if __name__ == "__main__" :
  # run the script!
  print("\nLaunching webcam... press `q` to quit.")
  main()
  print("Done.")

