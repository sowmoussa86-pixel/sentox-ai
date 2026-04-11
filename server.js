const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

// 👉 servir le frontend
app.use(express.static(path.join(__dirname, "public")));

// 👉 ANALYSE
app.post("/analyze", (req, res) => {
  const { product } = req.body;

  res.json({
    product,
    status: "Analysé",
    danger: "Faible",
    message: "Produit globalement sûr"
  });
});

// 👉 PDF
app.get("/pdf/:product", (req, res) => {
  const product = req.params.product;

  res.send(`
    <h1>Rapport SENTOX</h1>
    <p>Produit : ${product}</p>
    <p>Status : OK</p>
  `);
});

// 👉 fallback (important pour Render)
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log("Serveur lancé sur port " + PORT);
});