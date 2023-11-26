import os
import sys
from flask import (
    Flask,
    render_template,
)
sys.path.append('../')

app = Flask(__name__)
app.secret_key = os.urandom(24)

if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


@app.route("/")
def hello():
    return render_template("welcome.html")

@app.route("/victory", methods=["GET"])
def victory():
    return render_template("victory.html")

@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    return render_template("thumbsUp.html")

@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    return render_template("thumbsDown.html")

@app.route("/stop", methods=["GET"])
def stop():
    return render_template("stop.html")

@app.route("/rock", methods=["GET"])
def rock():
    return render_template("rock.html")
