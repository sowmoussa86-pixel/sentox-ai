const express = require("express");
const app = express();

const fs = require("fs");
const path = require("path");
const pdfParse = require("pdf-parse");

const data = require("./data/database.json");

// STATIC
app.use(express.static("public"));
app.use("/pdf", express.static("public/pdf"));

// SCORE
function calculateScore(dl50) {
  if (!dl50) return "Inconnu";

  if (dl50 < 50) return "Très élevé ⚠️";
  if (dl50 < 300) return "Élevé";
  if (dl50 < 2000) return "Modéré";
  return "Faible";
}

// EXTRACTION PDF
function extractToxicology(text) {
  return {
    dl50: text.match(/DL50[:\s]+(\d+)/i)?.[1] || "Non trouvé",
    toxicite: text.match(/toxicité[:\s]+([^\n]+)/i)?.[1] || "Non trouvé",
    organes: text.match(/foie|rein|cerveau|poumon/i)?.[0] || "Non trouvé"
  };
}

// SEARCH
app.get("/search", (req, res) => {
  const query = req.query.q?.toLowerCase();

  if (!query) {
    return res.json({ message: "Aucune recherche" });
  }

  const plant = data.plants.find(p =>
    p.nom_scientifique.toLowerCase().includes(query) ||
    p.nom_local.toLowerCase().includes(query)
  );

  if (plant) {
    return res.json({
      type: "plante",
      data: {
        ...plant,
        score: calculateScore(plant.dl50)
      }
    });
  }

  const med = data.medicaments.find(m =>
    m.nom_commercial.toLowerCase().includes(query) ||
    m.dci.toLowerCase().includes(query)
  );

  if (med) {
    return res.json({
      type: "medicament",
      data: {
        ...med,
        score: calculateScore(med.toxicologie?.dl50)
      }
    });
  }

  const sub = data.substances.find(s =>
    s.nom.toLowerCase().includes(query) ||
    s.cas.includes(query)
  );

  if (sub) {
    return res.json({
      type: "substance",
      data: {
        ...sub,
        score: calculateScore(sub.toxicologie?.dl50)
      }
    });
  }

  res.json({ message: "Produit non trouvé" });
});

// PDF DATA
app.get("/pdf-data", async (req, res) => {
  let file = req.query.file;

  if (!file) {
    return res.json({ error: "Aucun fichier fourni" });
  }

  if (!file.endsWith(".pdf")) {
    file += ".pdf";
  }

  try {
    const filePath = path.join(__dirname, "public", "pdf", file);

    const dataBuffer = fs.readFileSync(filePath);
    const pdf = await pdfParse(dataBuffer);

    const extracted = extractToxicology(pdf.text);

    res.json({
      extracted,
      preview: pdf.text.substring(0, 1000)
    });

  } catch (error) {
    console.error(error);
    res.json({ error: "PDF non trouvé ou erreur lecture" });
  }
});

// START
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log("Serveur lancé sur le port " + PORT);
});