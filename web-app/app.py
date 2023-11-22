from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.1')

@app.route('/')
def home():
    print("This message will be printed to the console.")
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    