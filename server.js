const express = require("express");
const app = express();
const path = require("path");

// servir les fichiers frontend
app.use(express.static("public"));

/* =========================
   LOGIQUE TOXICOLOGIQUE
========================= */
function analyseToxicologique(produit) {
    produit = produit.toLowerCase();

    if (produit.includes("paracetamol")) {
        return {
            nom: "Paracétamol",
            risque: "Faible à modéré",
            organe_cible: "Foie",
            dose_max: "4g/jour adulte",
            toxicite: "Hépatotoxicité en cas de surdosage",
            interactions: ["Alcool", "Isoniazide"],
            conseils: "Éviter l’alcool et respecter la dose",
            niveau: "🟢"
        };
    }

    if (produit.includes("ibuprofene")) {
        return {
            nom: "Ibuprofène",
            risque: "Modéré",
            organe_cible: "Estomac, reins",
            dose_max: "1200–2400 mg/jour",
            toxicite: "Ulcères et insuffisance rénale",
            interactions: ["Aspirine", "Anticoagulants"],
            conseils: "Prendre après repas",
            niveau: "🟠"
        };
    }

    return {
        nom: produit,
        risque: "Inconnu",
        organe_cible: "Non défini",
        dose_max: "Non disponible",
        toxicite: "Données insuffisantes",
        interactions: [],
        conseils: "Consulter un professionnel de santé",
        niveau: "⚪"
    };
}

/* =========================
   API ANALYSE
========================= */
app.get("/analyze", (req, res) => {
    const produit = req.query.produit;

    if (!produit) {
        return res.json({ erreur: "Produit non fourni" });
    }

    const resultat = analyseToxicologique(produit);
    res.json(resultat);
});

/* =========================
   PORT
========================= */
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log("Serveur lancé sur le port " + PORT);
});