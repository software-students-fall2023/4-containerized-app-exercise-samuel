FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . .

EXPOSE 8000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

