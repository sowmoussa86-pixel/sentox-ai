const express = require("express");
const app = express();
const PDFDocument = require("pdfkit");
const fetch = require("node-fetch");

app.use(express.static("public"));

/* =========================
   NORMALISATION TEXTE
========================= */
function nettoyer(texte) {
    return texte
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

/* =========================
   BASE PLANTES INTERNATIONALE
========================= */
const basePlantes = {
    neem: {
        nom: "Neem",
        dl50: "2000–5000 mg/kg",
        dose: "variable",
        usages: ["antipaludique", "antibactérien"],
        activites: ["anti-inflammatoire"],
        forme: ["huile", "infusion"],
        dosage: "non standardisé",
        toxicite: "toxique forte dose",
        score: 6
    },
    moringa: {
        nom: "Moringa",
        dl50: null,
        dose: "traditionnelle",
        usages: ["nutrition"],
        activites: ["antioxydant"],
        forme: ["feuilles"],
        dosage: null,
        toxicite: "faible",
        score: 2
    },
    kinkeliba: {
        nom: "Kinkeliba",
        dl50: null,
        dose: "infusion",
        usages: ["digestif"],
        activites: ["hépatoprotecteur"],
        forme: ["infusion"],
        dosage: "traditionnel",
        toxicite: "faible",
        score: 2
    }
};

/* =========================
   ANALYSE PLANTE
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
        dl50: plante.dl50 || "Études en cours",
        dose: plante.dose || "Non disponible",
        usages: plante.usages.join(", "),
        activites: plante.activites.join(", "),
        forme: plante.forme.join(", "),
        dosage: plante.dosage || "Études en cours",
        toxicite: plante.toxicite,
        risque: plante.score >= 7 ? "Élevé" :
                plante.score >= 4 ? "Modéré" : "Faible",
        niveau: plante.score >= 7 ? "🔴" :
                plante.score >= 4 ? "🟠" : "🟢",
        score: plante.score
    };
}

/* =========================
   API ANALYSE SIMPLE
========================= */
app.get("/analyze", (req, res) => {
    const produit = req.query.produit;
    res.json(analyserPlante(produit));
});

/* =========================
   API PUBCHEM (MONDIALE)
========================= */
app.get("/api/pubchem", async (req, res) => {
    const produit = req.query.produit;

    try {
        const url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${produit}/property/MolecularWeight/JSON`;

        const response = await fetch(url);
        const data = await response.json();

        res.json({
            source: "PubChem",
            data: data
        });

    } catch {
        res.json({
            message: "Données non disponibles (études en cours)"
        });
    }
});

/* =========================
   IA SCIENTIFIQUE
========================= */
app.get("/ai-science", (req, res) => {
    const produit = req.query.produit;

    res.json({
        analyse: `
Analyse scientifique du produit ${produit} :

- Toxicité dépend de la dose
- Effets possibles sur organes
- Interactions médicamenteuses possibles
- Données scientifiques en cours d’évolution

⚠️ Certaines données peuvent être en cours de validation.
`
    });
});

/* =========================
   ANALYSE COMPLETE
========================= */
app.get("/analyse-complete", async (req, res) => {
    const produit = req.query.produit;

    const local = analyserPlante(produit);

    let pubchem;

    try {
        const response = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${produit}/property/MolecularWeight/JSON`);
        pubchem = await response.json();
    } catch {
        pubchem = "Études en cours";
    }

    res.json({
        produit,
        local,
        pubchem
    });
});

/* =========================
   PDF
========================= */
app.get("/pdf", (req, res) => {
    const produit = req.query.produit;
    const data = analyserPlante(produit);

    const doc = new PDFDocument();

    res.setHeader("Content-Type", "application/pdf");
    doc.pipe(res);

    doc.fontSize(20).text("RAPPORT SENTOX", { align: "center" });

    doc.moveDown();
    doc.fontSize(12).text(`Produit: ${data.nom}`);
    doc.text(`Risque: ${data.risque}`);
    doc.text(`Score: ${data.score}/10`);
    doc.text(`DL50: ${data.dl50}`);
    doc.text(`Dose: ${data.dose}`);
    doc.text(`Usages: ${data.usages}`);
    doc.text(`Activités: ${data.activites}`);
    doc.text(`Forme: ${data.forme}`);
    doc.text(`Dosage: ${data.dosage}`);
    doc.text(`Toxicité: ${data.toxicite}`);

    doc.end();
});

/* ========================= */
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log("Serveur SENTOX lancé 🚀");
});