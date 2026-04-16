const express = require("express");
const app = express();
const path = require("path");

const data = require("./data/database.json");

app.use(express.static("public"));
app.use("/pdf", express.static(path.join(__dirname, "public/pdf")));


// 🔥 Fonction SCORE TOXICOLOGIQUE
function calculateScore(dl50) {
  if (!dl50) return "Inconnu";

  if (dl50 < 50) return "Très élevé ⚠️";
  if (dl50 < 300) return "Élevé";
  if (dl50 < 2000) return "Modéré";
  return "Faible";
}


// 🔍 ROUTE RECHERCHE UNIQUE
app.get("/search", (req, res) => {
  const query = req.query.q?.toLowerCase();

  if (!query) {
    return res.json({ message: "Aucune recherche" });
  }

  // 🌿 PLANTES
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

  // 💊 MEDICAMENTS
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

  // ☣️ SUBSTANCES
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

  // ❌ NON TROUVÉ
  res.json({ message: "Produit non trouvé" });
});


// 🚀 LANCEMENT SERVEUR
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Serveur lancé sur le port " + PORT);
});