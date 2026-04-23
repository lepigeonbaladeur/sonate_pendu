from flask import Flask, render_template, request
import string

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    if request.method == "POST":
        speudo = request.form["pseudo"]
    return render_template("play.html", clavier = string.ascii_uppercase)