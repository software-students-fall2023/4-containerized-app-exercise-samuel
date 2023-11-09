'''
Find available camera devices for opencv-python (i.e. cv2) to use.
Install dependencies and run this file:
  pipenv install
  pipenv run python find_camera_devices.py
'''

import cv2

def get_first_working_device_index():
    """
    Returns the first working camera device.
    """
    available_devices,working_devices,non_working_devices = list_camera_devices(quit_after_one=True)
    if len(working_devices) > 0:
      return working_devices[0]
    else:
      return None

def list_camera_devices(quit_after_one=False):
    """
    Test the devices and returns a tuple with the available devices and the ones that are working.
    @param quit_after_one: If True, the function will quit after the first working device is found.
    """
    working_devices = []
    available_devices = []
    non_working_devices = []
    device_index = 0 # start from device 0
    while len(non_working_devices) < 6: # if there are more than 5 non-working devices stop the testing. 
      print(f"\nDEVICE {device_index}:")
      camera = cv2.VideoCapture(device_index)
      if not camera.isOpened():
        # this device cannot be opened and is not working
        non_working_devices.append(device_index)
        print("Not working!")
      else:
        #this device can be opened... try to read from it...
        is_reading, img = camera.read()
        w = camera.get(3)
        h = camera.get(4)
        if is_reading:
          print(f"Available and ready to read images ({int(w)} x {int(h)}]).")
          working_devices.append(device_index)
          if quit_after_one:
            break  # quit the loop
        else:
          print(f"Available, but can't read images  ({int(w)} x {int(h)}]).")
          available_devices.append(device_index)
      device_index +=1 # iterate to the next device device
    return available_devices,working_devices,non_working_devices
    
if __name__ == '__main__':
  # try out the device devices
  available_devices,working_devices,non_working_devices = list_camera_devices()
  # print the results
  print()
  print('-'*20)
  print(f"Available devices: {available_devices}")
  print(f"Working devices: {working_devices}")
  print(f"Non working devices: {non_working_devices}")
  print('-'*20)
  print()
