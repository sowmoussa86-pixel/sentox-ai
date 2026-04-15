const express = require("express");
const app = express();
const PDFDocument = require("pdfkit");
const fetch = require("node-fetch");

app.use(express.static("public"));

/* =========================
   NORMALISATION
========================= */
function nettoyer(texte) {
    return texte
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

/* =========================
   BASE HYBRIDE (PLANTES + MEDICAMENTS)
========================= */
const basePlantes = {

    neem: {
        nom: "Neem",
        dl50: "2000–5000 mg/kg",
        dose: "variable",
        usages: ["antipaludique"],
        activites: ["anti-inflammatoire"],
        forme: ["huile", "infusion"],
        dosage: "non standardisé",
        toxicite: "toxique forte dose",
        score: 6
    },

    moringa: {
        nom: "Moringa",
        dl50: "Études en cours",
        dose: "traditionnelle",
        usages: ["nutrition"],
        activites: ["antioxydant"],
        forme: ["feuilles"],
        dosage: "traditionnel",
        toxicite: "faible",
        score: 2
    },

    paracetamol: {
        nom: "Paracétamol",
        dl50: "338 mg/kg",
        dose: "500 mg - 1g",
        usages: ["antalgique"],
        activites: ["analgésique"],
        forme: ["comprimé"],
        dosage: "max 4g/jour",
        toxicite: "hépatotoxique",
        score: 7
    }
};

/* =========================
   ANALYSE
========================= */
function analyserPlante(produit) {

    produit = nettoyer(produit);

    const plante = basePlantes[produit];

    if (!plante) {
        return {
            nom: produit,
            dl50: "Études en cours",
            dose: "Non disponible",
            usages: "Données insuffisantes",
            activites: "Non documenté",
            forme: "Non définie",
            dosage: "Études en cours",
            toxicite: "Inconnue",
            risque: "Inconnu",
            niveau: "⚪",
            score: 0
        };
    }

    return {
        nom: plante.nom,
        dl50: plante.dl50,
        dose: plante.dose,
        usages: plante.usages.join(", "),
        activites: plante.activites.join(", "),
        forme: plante.forme.join(", "),
        dosage: plante.dosage,
        toxicite: plante.toxicite,
        risque: plante.score >= 7 ? "Élevé" :
                plante.score >= 4 ? "Modéré" : "Faible",
        niveau: plante.score >= 7 ? "🔴" :
                plante.score >= 4 ? "🟠" : "🟢",
        score: plante.score
    };
}

/* =========================
   ROUTES
========================= */

// Analyse simple
app.get("/analyze", (req, res) => {
    res.json(analyserPlante(req.query.produit));
});

// PubChem
app.get("/api/pubchem", async (req, res) => {
    try {
        const r = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${req.query.produit}/property/MolecularWeight/JSON`);
        const data = await r.json();
        res.json(data);
    } catch {
        res.json({ message: "Études en cours" });
    }
});

// PubMed
app.get("/api/pubmed", async (req, res) => {
    try {
        const r = await fetch(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${req.query.produit}&retmode=json`);
        const data = await r.json();
        res.json(data);
    } catch {
        res.json({ message: "Études en cours" });
    }
});

// IA
app.get("/ai", (req, res) => {
    const data = analyserPlante(req.query.produit);

    let interpretation =
        data.score >= 7 ? "Risque élevé" :
        data.score >= 4 ? "Risque modéré" :
        "Risque faible";

    res.json({
        produit: data.nom,
        interpretation
    });
});

// FULL AI (TOUT)
app.get("/full-ai", async (req, res) => {

    const produit = req.query.produit;

    const local = analyserPlante(produit);

    let pubchem;
    let pubmed;

    try {
        const r1 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${produit}/property/MolecularWeight/JSON`);
        pubchem = await r1.json();
    } catch {
        pubchem = "Études en cours";
    }

    try {
        const r2 = await fetch(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${produit}&retmode=json`);
        pubmed = await r2.json();
    } catch {
        pubmed = "Études en cours";
    }

    res.json({
        produit,
        local,
        pubchem,
        pubmed
    });
});

// PDF
app.get("/pdf", (req, res) => {
    const data = analyserPlante(req.query.produit);

    const doc = new PDFDocument();
    res.setHeader("Content-Type", "application/pdf");

    doc.pipe(res);

    doc.text("RAPPORT SENTOX");
    doc.text(`Produit: ${data.nom}`);
    doc.text(`Risque: ${data.risque}`);
    doc.text(`Score: ${data.score}/10`);

    doc.end();
});

/* ========================= */
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log("SENTOX lancé 🚀");
});