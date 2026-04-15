const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.static("public"));

/* ============================
   BASE DE DONNÉES SCIENTIFIQUE
============================ */

const db = {
  neem: {
    nom: "Neem",
    risque: "Modéré",
    score: 6,
    dl50: "200 mg/kg",
    dose: "500 mg/jour",
    usages: "Antipaludique, antibactérien",
    activites: "Antifongique, anti-inflammatoire",
    forme: "Extrait, poudre",
    dosage: "1-2 prises/jour",
    toxicite: "Toxique à forte dose"
  },

  paracetamol: {
    nom: "Paracétamol",
    risque: "Faible",
    score: 3,
    dl50: "338 mg/kg",
    dose: "500-1000 mg",
    usages: "Antalgique, antipyrétique",
    activites: "Inhibition COX",
    forme: "Comprimé, sirop",
    dosage: "Max 4g/jour",
    toxicite: "Hépatotoxique à forte dose"
  },

  moringa: {
    nom: "Moringa",
    risque: "Faible",
    score: 2,
    dl50: "Études en cours",
    dose: "500-1000 mg",
    usages: "Nutrition, antioxydant",
    activites: "Anti-inflammatoire",
    forme: "Poudre, capsule",
    dosage: "1-2 fois/jour",
    toxicite: "Faible"
  }
};

/* ============================
   ANALYSE SIMPLE
============================ */

app.get("/analyze", (req, res) => {
  let p = (req.query.produit || "").toLowerCase();

  if (db[p]) {
    res.json(db[p]);
  } else {
    res.json({
      nom: p,
      risque: "Inconnu",
      score: 0,
      dl50: "Études en cours",
      dose: "Non disponible",
      usages: "Données insuffisantes",
      activites: "Non documenté",
      forme: "Non définie",
      dosage: "Études en cours",
      toxicite: "Inconnue"
    });
  }
});

/* ============================
   IA INTERPRÉTATION
============================ */

app.get("/ai", (req, res) => {
  let p = (req.query.produit || "").toLowerCase();
  let data = db[p];

  if (!data) {
    return res.json({
      interpretation: "Produit inconnu. Données scientifiques insuffisantes."
    });
  }

  let interpretation = `Le produit ${data.nom} présente un risque ${data.risque}. 
Score toxicologique: ${data.score}/10. 
Toxicité: ${data.toxicite}. 
Utilisation recommandée avec précaution.`;

  res.json({ interpretation });
});

/* ============================
   PDF SIMPLE
============================ */

app.get("/pdf", (req, res) => {
  let p = (req.query.produit || "").toLowerCase();
  let d = db[p];

  if (!d) return res.send("Produit non trouvé");

  res.send(`
    <h1>RAPPORT SENTOX</h1>
    <p>Produit: ${d.nom}</p>
    <p>Risque: ${d.risque}</p>
    <p>Score: ${d.score}/10</p>
    <p>DL50: ${d.dl50}</p>
    <p>Dose: ${d.dose}</p>
    <p>Usages: ${d.usages}</p>
    <p>Activités: ${d.activites}</p>
    <p>Forme: ${d.forme}</p>
    <p>Dosage: ${d.dosage}</p>
    <p>Toxicité: ${d.toxicite}</p>
  `);
});

/* ============================
   LANCEMENT
============================ */

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Serveur lancé sur port " + PORT));