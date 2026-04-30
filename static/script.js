let lettresDejaDites = [];

function devinerLettre(lettre, bouton) {
  if (lettresDejaDites.includes(lettre)) lettresDejaDites.push(lettre);
  bouton.disabled = true;
  bouton.classList.add("btn-used");
  fetch("/guess", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: "lettre=" + lettre,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById("score").textContent = "Score:" + data.score;
      let affichage = "";
      for (let lettre of data.mot) {
        if (data.lettres_trouvees.includes(lettre)) {
          affichage += lettre + " ";
        } else {
          affichage += " _ ";
        }
      }
      document.getElementById("mot").textContent = affichage;

      let coeurs = "";
      for (let i = 0; i < data.vies; i++) {
        coeurs += "🖤";
      }
      document.getElementById("vies").textContent = coeurs;

      if (data.vies === 4) {
        document.getElementById("base").classList.add("visible");
      } else if (data.vies === 3) {
        document.getElementById("poutre").classList.add("visible");
      } else if (data.vies === 2) {
        document.getElementById("tete").classList.add("visible");
      } else if (data.vies === 1) {
        document.getElementById("corps").classList.add("visible");
      } else if (data.vies === 0) {
        document.getElementById("membres").classList.add("visible");
      }

      if (data.gameover) {
        window.location.href = "/gameover";
      }
      if (data.victoire) {
        document.getElementById("winner").style.display = "block";
      }
    });
}

function motSuivant() {
  fetch("/next")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("winner").style.display = "none";
      let affichage = "";
      for (let lettre of data.mot) {
        affichage += " _ ";
      }
      document.getElementById("mot").textContent = affichage;
      document.querySelectorAll(".btn-letter").forEach((btn) => {
        btn.disabled = false;
        btn.classList.remove("btn-used");
      });
      document.getElementById("base").classList.remove("visible");
      document.getElementById("poutre").classList.remove("visible");
      document.getElementById("tete").classList.remove("visible");
      document.getElementById("corps").classList.remove("visible");
      document.getElementById("membres").classList.remove("visible");
      let coeurs = "";
      for (let i = 0; i < data.vies; i++) {
        coeurs += "🖤";
      }
      document.getElementById("vies").textContent = coeurs;
    });
}

function ouverture(nomPotence, nomBouton) {
  let potence = document.getElementById(nomPotence);
  let bouton = document.getElementById(nomBouton);
  potence.classList.toggle("ouvert");
  if (potence.classList.contains("ouvert")) {
    bouton.innerHTML = "&#x226B;";
  } else {
    bouton.innerHTML = "&#x226A;";
  }
}

const jauge = document.getElementById("volume-slider");
const musique = document.getElementById("volume");
jauge.addEventListener("input", function () {
  musique.volume = jauge.value;
});

for (let i = 0; i < 50; i++) {
  let etoile = document.createElement("div");
  etoile.textContent = "✦";
  etoile.style.position = "absolute";
  etoile.style.top = Math.random() * 100 + "%";
  etoile.style.left = Math.random() * 100 + "%";
  etoile.style.color = "#FFB000";
  etoile.style.fontSize = Math.random() * 20 + 10 + "px";
  etoile.style.zIndex = "-1";
  document.body.appendChild(etoile);
}
