[![CI Badge](https://github.com/software-students-fall2023/4-containerized-app-exercise-samuel/actions/workflows/Main.yaml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-samuel/actions/workflows/Main.yaml)


# Real-Time Hand Gesture Recognition Webapp

## Team Members

- [Ana Sofia](https://github.com/anaspacheco)
- [Samuel Shally ](https://github.com/SamuelShally)
- [Lemon](https://github.com/Lefie)

## Project Description 

Our project is a Real-Time Hand Gesture Recognition Webapp. The web application is designed to recognize hand gestures in real-time using computer vision and machine learning techniques. Users can interact with the application by performing various hand gestures, and at the end, you will see what image corresponds with the gesture you did the most. Beware that, since it takes 1 frame per second, it may seem a bit slow.

## Setup Instructions

1. **Create `.env` file with the following fields:**
   
    ```
    MONGO_URI="mongodb://localhost:27017/"
    MONGO_DBNAME={example-name}
    FLASK_APP=app.py
    FLASK_ENV=development
    ```

2. **Cd to the repository:**
   
    ```bash
    cd path/to/your/localrepository
    ```

3. **Install Docker Desktop:**
   
    [Docker Desktop Installation Guide](https://www.docker.com/products/docker-desktop)

4. **Run the following command to build and start the application using Docker Compose:**
   
    ```bash
    docker-compose up --build
    ```
5. **Adjust mediapipe package in requirements.txt to match your python version**

   ```bash
   latest: mediapipe==0.10.8
   ```

5. **Access the web-app:**
   
    Open your web browser and go to [http://localhost:5002](http://localhost:5002).

### Optional: Pull from the latest hosted images
```
docker pull samuelshally/4-containerized-app-exercise-samuel-web_app:latest

docker pull samuelshally/4-containerized-app-exercise-samuel-machine_learning_client:latest

docker pull samuelshally/mongo:latest
```




  
