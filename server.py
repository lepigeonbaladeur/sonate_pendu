from flask import Flask, render_template, request, session, redirect, jsonify
import string
import random
import unicodedata



app = Flask(__name__)

app.secret_key = "a847v7Pr$PD8!rhsv!w8B6Jfrx*7wY422ne*"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    session['vies'] = 5
    session['lettres_trouvees']= []
    session['score'] = 0
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
    return render_template("play.html", clavier = string.ascii_uppercase,pseudo = pseudo, mot=mot, lettres_trouvees=session['lettres_trouvees'],score=session['score'],  vies=session['vies'])



@app.route('/guess', methods=["POST"])
def guess():
    lettre = request.form["lettre"]
    mot = session['mot'].upper()
    if lettre in mot:
        session['lettres_trouvees'].append(lettre)
        session['score'] += 10
        session.modified = True
    else:
        session['vies'] -= 1
    lignes = []
    if set(session['lettres_trouvees']) == len(set(mot)):
        mot = session['mot'].upper()
        session['lettres_trouvees']= []
        fichier = r"./dictionnaire.txt"
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.rstrip().split(";")[0]
                ligne = unicodedata.normalize('NFKD', ligne).encode('ASCII', 'ignore').decode('ASCII')
                lignes.append(ligne)
        mot=random.choice(lignes)
        session['mot'] = mot
    return jsonify({"score": session['score'],"vies": session['vies'],"lettres_trouvees": session['lettres_trouvees'],"mot": session['mot'].upper(),"gameover": session['vies'] == 0, "victoire": len(session['lettres_trouvees'])== len (set(mot))})

@app.route('/gameover', methods=["POST", "GET"])
def gammeover():
    pseudo = session["pseudo"]
    return render_template("gameover.html", pseudo=pseudo, score=session['score'])

@app.route('/next', methods=["POST", "GET"])
def next():
    session['vies'] = 5
    session['lettres_trouvees'] = []
    session.modified = True
    fichier = r"./dictionnaire.txt"
    lignes = []
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.rstrip().split(";")[0]
            ligne = unicodedata.normalize('NFKD', ligne).encode('ASCII', 'ignore').decode('ASCII')
            lignes.append(ligne)
    mot=random.choice(lignes)
    session['mot'] = mot
    return jsonify({"mot": session['mot'].upper(), "vies": session['vies']})

  