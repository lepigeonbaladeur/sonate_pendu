from flask import Flask, render_template, request, session
import string
import random



app = Flask(__name__)

app.secret_key = "a847v7Pr$PD8!rhsv!w8B6Jfrx*7wY422ne*"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    session['vies'] = 5
    session['lettres_trouvees']= []
    fichier = r"./dictionnaire.txt"
    lignes = []
    f = open(fichier, "r", encoding="utf-8")
    for ligne in f:
        ligne = ligne.rstrip().split(";")[0]
        lignes.append(ligne) 
    f.close()
    mot=random.choice(lignes)
    pseudo = request.form["pseudo"]
    session['mot'] = mot
    session['pseudo'] = pseudo
    return render_template("play.html", clavier = string.ascii_uppercase,pseudo = pseudo, mot=mot, lettres_trouvees=session['lettres_trouvees'])



@app.route('/guess', methods=["POST"])
def guess():
    pseudo = session["pseudo"]
    lettre = request.form["lettre"]
    mot = session['mot'].upper()
    if lettre in mot:
        session['lettres_trouvees'].append(lettre)
        session.modified = True
    else:
        session['vies'] -= 1
    return render_template("play.html", clavier = string.ascii_uppercase,pseudo = pseudo, mot=mot, lettres_trouvees=session['lettres_trouvees'])

