const express = require("express");
const fs = require("fs");
const path = require("path");
const fetch = require("node-fetch");

const app = express();
app.use(express.static("public"));

// 📁 Charger base locale
const database = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, "data", "database.json"),
    "utf-8"
  )
);

// 🧪 PubChem
async function getPubChem(produit) {
  try {
    const url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${produit}/property/MolecularFormula,MolecularWeight/JSON`;
    const res = await fetch(url);
    const data = await res.json();

    const props = data.PropertyTable.Properties[0];

    return {
      formule: props.MolecularFormula,
      poids: props.MolecularWeight
    };
  } catch {
    return { formule: "N/A", poids: "N/A" };
  }
}

// 📚 PubMed
async function getPubMed(produit) {
  try {
    const url = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${produit}&retmode=json`;
    const res = await fetch(url);
    const data = await res.json();

    return data.esearchresult.idlist.length + " articles";
  } catch {
    return "N/A";
  }
}

// 🔍 Analyse complète
app.get("/analyze", async (req, res) => {
  const produit = req.query.produit.toLowerCase();

  const local = database.find(p =>
    produit.includes(p.nom.toLowerCase())
  );

  const pubchem = await getPubChem(produit);
  const pubmed = await getPubMed(produit);

  res.json({
    nom: produit,
    risque: local?.risque || "Inconnu",
    score: local?.score || "0/10",
    toxicite: local?.toxicite || "Non documentée",

    formule: pubchem.formule,
    poids: pubchem.poids,
    pubmed: pubmed
  });
});

// 📄 PDF LOCAL
app.get("/pdf-local", (req, res) => {
  const produit = req.query.produit.toLowerCase();

  const data = database.find(p =>
    produit.includes(p.nom.toLowerCase())
  );

  if (!data || !data.pdf) {
    return res.send("PDF non disponible");
  }

  const filePath = path.join(__dirname, "pdfs", data.pdf);
  res.sendFile(filePath);
});

// 🚀 Lancement
app.listen(3000, () => {
  console.log("SENTOX actif sur http://localhost:3000");
});