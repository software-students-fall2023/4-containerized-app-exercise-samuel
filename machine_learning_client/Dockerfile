FROM python:3.8-slim

WORKDIR /machine_learning_client

COPY . /app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "setup.py"]

