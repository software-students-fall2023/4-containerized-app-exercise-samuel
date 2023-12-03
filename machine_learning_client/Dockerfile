FROM python:3.8-slim

WORKDIR /machine_learning_client

# Print the current directory content
RUN ls -al

COPY . .

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "setup.py"]


