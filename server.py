from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    if request.method == "POST":
        speudo = request.form["pseudo"]
    return render_template("play.html")