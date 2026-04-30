from flask import Flask, render_template, request, session, redirect, jsonify
from dotenv import load_dotenv

import os
import string
import random
import unicodedata

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


def set_session_variables(values):
    for key, val in values.items():
        session[key] = val


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/play", methods=["POST"])
def play():
    fichier = r"./dictionnaire.txt"
    lignes = []
    f = open(fichier, "r", encoding="utf-8")

    for ligne in f:
        ligne = ligne.rstrip().split(";")[0]
        lignes.append(ligne)
    f.close()

    mot = random.choice(lignes)
    pseudo = request.form["pseudo"]

    # Définir en lot les variables de session
    session_values = {
        "vies": 5,
        "lettres_trouvees": [],
        "score": 0,
        "pseudo": pseudo,
        "mot": mot,
    }
    set_session_variables(session_values)

    return render_template(
        "play.html",
        clavier=string.ascii_uppercase,
        pseudo=pseudo,
        mot=mot,
        lettres_trouvees=session["lettres_trouvees"],
        score=session["score"],
        vies=session["vies"],
    )


@app.route("/guess", methods=["POST"])
def guess():
    lettre = request.form["lettre"]
    mot = session["mot"].upper()

    if lettre in mot:
        session["lettres_trouvees"].append(lettre)
        session["score"] += 10
        session.modified = True
    else:
        session["vies"] -= 1

    lignes = []

    if set(session["lettres_trouvees"]) == len(set(mot)):
        mot = session["mot"].upper()
        session["lettres_trouvees"] = []
        fichier = r"./dictionnaire.txt"

        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.rstrip().split(";")[0]
                ligne = (
                    unicodedata.normalize("NFKD", ligne)
                    .encode("ASCII", "ignore")
                    .decode("ASCII")
                )
                lignes.append(ligne)
        mot = random.choice(lignes)
        session["mot"] = mot

    return jsonify(
        {
            "score": session["score"],
            "vies": session["vies"],
            "lettres_trouvees": session["lettres_trouvees"],
            "mot": session["mot"].upper(),
            "gameover": session["vies"] == 0,
            "victoire": len(session["lettres_trouvees"]) == len(set(mot)),
        }
    )


@app.route("/gameover", methods=["POST", "GET"])
def gammeover():
    pseudo = session["pseudo"]
    return render_template("gameover.html", pseudo=pseudo, score=session["score"])


@app.route("/next", methods=["POST", "GET"])
def next():
    session["vies"] = 5
    session["lettres_trouvees"] = []
    session.modified = True
    fichier = r"./dictionnaire.txt"
    lignes = []
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.rstrip().split(";")[0]
            ligne = (
                unicodedata.normalize("NFKD", ligne)
                .encode("ASCII", "ignore")
                .decode("ASCII")
            )
            lignes.append(ligne)
    mot = random.choice(lignes)
    session["mot"] = mot
    return jsonify({"mot": session["mot"].upper(), "vies": session["vies"]})
