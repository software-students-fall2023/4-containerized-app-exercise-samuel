FROM python:3.8-slim

WORKDIR /machine_learning_client

COPY machine_learning_client/ ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt && \
    apt-get install -y libgl1-mesa-glx && \
    pip install opencv-python-y

EXPOSE 9090

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]