"""
Does a thing. 
"""

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
    """
    Does a thing. 
    """
    return render_template("welcome.html")

@app.route("/victory", methods=["GET"])
def victory():
    """
    Does a thing. 
    """
    return render_template("victory.html")

@app.route("/thumbsUp", methods=["GET"])
def thumbs_up():
    """
    Does a thing. 
    """
    return render_template("thumbsUp.html")

@app.route("/thumbsDown", methods=["GET"])
def thumbs_down():
    """
    Does a thing. 
    """
    return render_template("thumbsDown.html")

@app.route("/stop", methods=["GET"])
def stop():
    """
    Does a thing. 
    """
    return render_template("stop.html")

@app.route("/rock", methods=["GET"])
def rock():
    """
    Does a thing. 
    """
    return render_template("rock.html")
