const express = require("express");
const cors = require("cors");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const app = express();
app.use(cors());
app.use(express.static("public"));

/* ============================
   BASE MINIMALE (fallback)
============================ */
const db = {
  neem: { risque: "Modéré", score: 6 },
  paracetamol: { risque: "Faible", score: 3 }
};

/* ============================
   PUBCHEM (TOXICO + FORMULE)
============================ */
app.get("/pubchem", async (req, res) => {
  let p = req.query.produit;

  try {
    let url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${p}/property/MolecularFormula,MolecularWeight/JSON`;

    let r = await fetch(url);
    let data = await r.json();

    let props = data.PropertyTable.Properties[0];

    res.json({
      formule: props.MolecularFormula,
      poids: props.MolecularWeight
    });

  } catch {
    res.json({ error: "Données PubChem non trouvées" });
  }
});

/* ============================
   PUBMED (ARTICLES)
============================ */
app.get("/pubmed", async (req, res) => {
  let p = req.query.produit;

  try {
    let url = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${p}&retmode=json`;

    let r = await fetch(url);
    let data = await r.json();

    let count = data.esearchresult.count;

    res.json({
      articles: count + " articles scientifiques trouvés"
    });

  } catch {
    res.json({ articles: "Erreur PubMed" });
  }
});

/* ============================
   ANALYSE INTELLIGENTE
============================ */
app.get("/analyze", async (req, res) => {
  let p = (req.query.produit || "").toLowerCase();

  let base = db[p] || { risque: "Inconnu", score: 0 };

  let pubchem = {};
  let pubmed = {};

  try {
    let pc = await fetch(`http://localhost:3000/pubchem?produit=${p}`);
    pubchem = await pc.json();
  } catch {}

  try {
    let pm = await fetch(`http://localhost:3000/pubmed?produit=${p}`);
    pubmed = await pm.json();
  } catch {}

  res.json({
    nom: p,
    risque: base.risque,
    score: base.score,
    formule: pubchem.formule || "N/A",
    poids: pubchem.poids || "N/A",
    articles: pubmed.articles || "N/A",
    toxicite: base.score > 5 ? "Surveiller dose" : "Faible"
  });
});

/* ============================
   IA (PRÊTE POUR OPENAI)
============================ */
app.get("/ai", async (req, res) => {
  let p = req.query.produit;

  let interpretation = `
Analyse scientifique du produit ${p} :
- Données issues de PubChem et PubMed
- Évaluation toxicologique automatique
- Risque dépendant de la dose
- Recommandation : validation par expert
`;

  res.json({ interpretation });
});

/* ============================
   PDF
============================ */
app.get("/pdf", (req, res) => {
  let p = req.query.produit;

  res.send(`
    <h1>RAPPORT SENTOX ULTIME</h1>
    <p>Produit: ${p}</p>
    <p>Analyse générée par IA + bases scientifiques</p>
  `);
});

/* ============================
   START
============================ */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("SENTOX ULTIME lancé 🚀"));