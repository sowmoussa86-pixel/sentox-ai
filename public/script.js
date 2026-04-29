const API = "https://sentox-ai-backend.onrender.com"; // ton backend

const input = document.getElementById("searchInput");
const resultDiv = document.getElementById("results");

const btnSearch = document.getElementById("btnSearch");
const btnInteraction = document.getElementById("btnInteraction");
const btnFiche = document.getElementById("btnFiche");

// 👉 RECHERCHE
btnSearch.addEventListener("click", async () => {
  const val = input.value.trim();

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/search?nom=${val});
    const data = await res.json();

    resultDiv.innerHTML = <div class="card">${JSON.stringify(data)}</div>;
  } catch (e) {
    resultDiv.innerHTML = "Erreur serveur";
  }
});

// 👉 INTERACTION
btnInteraction.addEventListener("click", async () => {
  const val = input.value.trim();

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/interaction?nom=${val});
    const data = await res.json();

    resultDiv.innerHTML = <div class="card">${JSON.stringify(data)}</div>;
  } catch (e) {
    resultDiv.innerHTML = "Erreur interaction";
  }
});

// 👉 FICHE COMPLETE
btnFiche.addEventListener("click", async () => {
  const val = input.value.trim();

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/fiche?nom=${val});
    const data = await res.json();

    resultDiv.innerHTML = <div class="card">${JSON.stringify(data)}</div>;
  } catch (e) {
    resultDiv.innerHTML = "Erreur fiche";
  }
});