# base this image on a Debian release with Python installed
FROM python:3.9-bullseye 

# update the package manager
RUN apt update -y
RUN apt upgrade -y

# install the OpenCV cv2 dependencies missing from the Docker image
RUN apt install -y ffmpeg libsm6 libxext6  -y

# install the ALSA sound drivers missing from the Docker image
# RUN apt-get install -y alsa-base alsa-utils
RUN apt install -y alsa-utils

# install PortAudio library used by Python sounddevice
RUN apt install -y libportaudio2

# install the Python dependencies
RUN apt install -y cmake
RUN python -m pip install --upgrade pip
# RUN python -m pip install -U cmake

# RUN pip install pipenv

# create a directory for the app
RUN mkdir /app

# make the app directory the current working directory within the image
WORKDIR /app

# create a non-root user to use when running the container
# our use of `&&` helps with caching
RUN useradd -m -r beetroot && chown beetroot /app

# switch to our non-root user
USER beetroot

# copy the Pipfiles and install the dependencies... doing this fist may save build time via caching
# COPY Pipfile* .
COPY requirements.txt .

# install the app dependencies
#RUN pipenv install
RUN python -m pip install -r requirements.txt
RUN python -m pip install --upgrade numpy

# copy all the files from the current directory to the app directory
COPY . .

# when a container is instantiated, run the target script
# CMD ["pipenv", "run", "python", "find_camera_devices.py"]
CMD ["python", "find_camera_devices.py"]

