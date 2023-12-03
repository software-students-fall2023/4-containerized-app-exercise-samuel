FROM python:3.8-slim-buster

WORKDIR /web_app

COPY . .

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]