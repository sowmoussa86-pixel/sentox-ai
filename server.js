const express = require("express");
const app = express();
const PDFDocument = require("pdfkit");
function nettoyer(texte) {
    return texte
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}
// servir frontend
app.use(express.static("public"));

/* =========================
   BASE TOXICOLOGIQUE
========================= */
function analyseToxicologique(produit) {

    produit = nettoyer(produit);


    if (produit.includes("paracetamol")) {
        return {
            nom: "Paracétamol",
            risque: "Faible à modéré",
            organe_cible: "Foie",
            dose_max: "4g/jour",
            toxicite: "Hépatotoxicité",
            interactions: ["Alcool"],
            conseils: "Respecter la dose",
            niveau: "🟢",
            score: 2
        };
    }

    if (produit.includes("ibuprofene")) {
        return {
            nom: "Ibuprofène",
            risque: "Modéré",
            organe_cible: "Estomac",
            dose_max: "1200–2400 mg",
            toxicite: "Ulcères",
            interactions: ["Aspirine"],
            conseils: "Après repas",
            niveau: "🟠",
            score: 5
        };
    }

    if (produit.includes("kinkeliba")) {
        return {
            nom: "Kinkeliba",
            risque: "Faible",
            organe_cible: "Foie",
            dose_max: "Infusion",
            toxicite: "Faible",
            interactions: [],
            conseils: "Usage modéré",
            niveau: "🟢",
            score: 2
        };
    }

    if (produit.includes("neem")) {
        return {
            nom: "Neem",
            risque: "Modéré",
            organe_cible: "Foie",
            dose_max: "Contrôlé",
            toxicite: "Toxique forte dose",
            interactions: [],
            conseils: "Attention enfants",
            niveau: "🟠",
            score: 6
        };
    }

    return {
        nom: produit,
        risque: "Inconnu",
        organe_cible: "Non défini",
        dose_max: "Non disponible",
        toxicite: "Données insuffisantes",
        interactions: [],
        conseils: "Consulter un professionnel",
        niveau: "⚪",
        score: 0
    };
}

/* =========================
   API ANALYSE
========================= */
app.get("/analyze", (req, res) => {
    const produit = req.query.produit;
    res.json(analyseToxicologique(produit));
});

/* =========================
   IA SIMPLE
========================= */
app.get("/ai", (req, res) => {
    const produit = req.query.produit;

    res.json({
        message: `Analyse IA de ${produit} : vérifier toxicité, dose et interactions.`
    });
});

/* =========================
   PDF
========================= */
app.get("/pdf", (req, res) => {
    const produit = req.query.produit;
    const data = analyseToxicologique(produit);

    const doc = new PDFDocument();

    res.setHeader("Content-Type", "application/pdf");
    doc.pipe(res);

    doc.fontSize(20).text("RAPPORT SENTOX", { align: "center" });

    doc.moveDown();
    doc.fontSize(12).text(`Produit: ${data.nom}`);
    doc.text(`Risque: ${data.risque}`);
    doc.text(`Score: ${data.score}/10`);
    doc.text(`Organe: ${data.organe_cible}`);
    doc.text(`Dose max: ${data.dose_max}`);
    doc.text(`Toxicité: ${data.toxicite}`);
    doc.text(`Interactions: ${data.interactions.join(", ")}`);
    doc.text(`Conseils: ${data.conseils}`);

    doc.end();
});

/* ========================= */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Serveur lancé"));