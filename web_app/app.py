"""
Front end web page routes
"""

import os
import sys
from flask import (
    Flask,
    render_template,
)

sys.path.append("../")

app = Flask(__name__)
app.secret_key = os.urandom(24)

if os.getenv("FLASK_ENV", "development") == "development":
    app.debug = True


@app.route("/")
def hello():
    """
    Welcome page which starts the app.
    """
    return render_template("welcome.html")


@app.route("/victory", methods=["GET"])
def victory():
    """
    Pull the picture of churchill on victory gesture
    """
    return render_template("victory.html")


@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    """
    Pulls the picture of jesus on thumbs up gesture
    """
    return render_template("thumbsUp.html")


@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    """
    Pulls a picture of the devil on thumbs down gesture
    """
    return render_template("thumbsDown.html")


@app.route("/stop", methods=["GET"])
def stop():
    """
    Pull a picture of a snail on open palm gesture
    """
    return render_template("stop.html")


@app.route("/rock", methods=["GET"])
def rock():
    """
    Pulls a picture of a rock on closed fist gesture
    """
    return render_template("rock.html")
