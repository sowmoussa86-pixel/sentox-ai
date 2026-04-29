const API = "https://sentox-ai-backend.onrender.com";

const input = document.getElementById("searchInput");
const resultDiv = document.getElementById("results");

// 🔎 RECHERCHE
async function search() {
  const val = input.value.trim();
  resultDiv.innerHTML = "Chargement...";

  const res = await fetch(API + "/search?nom=" + val);
  const data = await res.json();

  let html = "";

  data.data.forEach(item => {
    html += `
      <div class="card">
        <h2>${item.nom}</h2>
        <p><b>Type:</b> ${item.type}</p>
        <p><b>Description:</b> ${item.description || ""}</p>
        <p><b>Toxicologie:</b> ${item.toxicologie || ""}</p>
      </div>
    `;
  });

  resultDiv.innerHTML = html;
}

// ⚗️ INTERACTION
async function interaction() {
  const val = input.value.trim();

  const res = await fetch(API + "/interaction?nom=" + val);
  const data = await res.json();

  resultDiv.innerHTML = `
    <div class="card">
      <h2>Interaction</h2>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    </div>
  `;
}

// 📄 FICHE
async function fiche() {
  const val = input.value.trim();

  const res = await fetch(API + "/fiche?nom=" + val);
  const data = await res.json();

  resultDiv.innerHTML = `
    <div class="card">
      <h2>Fiche complète</h2>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    </div>
  `;
}

// 📥 PDF
function pdf() {
  const val = input.value.trim();
  window.open(API + "/pdf/" + val, "_blank");
}

// 🧠 IA TOXICOLOGIE
async function ia() {
  const val = input.value.trim();
  resultDiv.innerHTML = "Analyse IA en cours...";

  const res = await fetch(API + "/ai?nom=" + val);
  const data = await res.json();

  resultDiv.innerHTML = `
    <div class="card">
      <h2>Analyse IA</h2>
      <p>${data.result}</p>
    </div>
  `;
}

// 🔗 BIND BOUTONS
document.getElementById("btnSearch").onclick = search;
document.getElementById("btnInteraction").onclick = interaction;
document.getElementById("btnFiche").onclick = fiche;
document.getElementById("btnPDF").onclick = pdf;
document.getElementById("btnIA").onclick = ia;