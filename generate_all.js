const fs = require("fs");

let db = require("./data/database.json");

// 🌿 PLANTES
let plants = [];
for (let i = 0; i < 100; i++) {
  plants.push({
    id: i + 1,
    nom_scientifique: "Plant_" + (i + 1),
    nom_local: "Local_" + (i + 1),
    partie_utilisee: "Feuilles",
    principe_actif: "Composé actif",
    indication: "Usage traditionnel",
    toxicite: i % 2 === 0 ? "Faible" : "Modérée",
    dose: "Infusion",
    dl50: 1000 + i * 50,
    risque: "Modéré",
    pdf: "plant" + (i + 1) + ".pdf"
  });
}

// 💊 MÉDICAMENTS
let medicaments = [];
for (let i = 0; i < 100; i++) {
  medicaments.push({
    id: i + 1,
    nom_commercial: "Med_" + (i + 1),
    dci: "DCI_" + (i + 1),
    classe: "Classe thérapeutique",
    chimie: {
      formule: "C" + (5 + i) + "H" + (10 + i),
      cas: "100-00-" + i
    },
    toxicologie: {
      dl50: 100 + i * 20,
      organes_cibles: "Foie"
    },
    pdf: "med" + (i + 1) + ".pdf"
  });
}

// ☣️ SUBSTANCES
let substances = [];
for (let i = 0; i < 100; i++) {
  substances.push({
    id: i + 1,
    nom: "Substance_" + (i + 1),
    cas: "200-00-" + i,
    famille: "Famille chimique",
    physicochimie: {
      formule: "C" + (3 + i) + "H" + (6 + i)
    },
    toxicologie: {
      dl50: 200 + i * 30
    },
    pdf: "sub" + (i + 1) + ".pdf"
  });
}

// 🔥 REMPLACER BASE
db.plants = plants;
db.medicaments = medicaments;
db.substances = substances;

// 💾 SAUVEGARDE
fs.writeFileSync(
  "./data/database.json",
  JSON.stringify(db, null, 2)
);

console.log("✅ 300 éléments générés !");