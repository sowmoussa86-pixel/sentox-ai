const API = "https://sentox-ai-backend.onrender.com";

const input = document.querySelector("input");
const btnSearch = document.querySelector("button:nth-of-type(1)");
const btnInteraction = document.querySelector("button:nth-of-type(2)");
const btnFiche = document.querySelector("button:nth-of-type(3)");

// 🔍 RECHERCHE
btnSearch.addEventListener("click", async () => {
  const val = input.value;

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/search?nom=${encodeURIComponent(val)});
    const data = await res.json();

    if (data.data && data.data.length > 0) {
      const item = data.data[0];

      document.getElementById("results").innerHTML = `
        <div class="card">
          <h3>${item.nom}</h3>
          <p>${item.description}</p>
        </div>
      `;
    } else {
      document.getElementById("results").innerHTML = "Aucun résultat";
    }

  } catch {
    document.getElementById("results").innerHTML = "Erreur serveur";
  }
});

// ⚗️ INTERACTION
btnInteraction.addEventListener("click", async () => {
  const val = input.value;

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/interaction?nom=${encodeURIComponent(val)});
    const data = await res.json();

    document.getElementById("results").innerHTML = `
      <div class="card">
        <h3>Interaction</h3>
        <p>${data.result || "Aucune interaction"}</p>
      </div>
    `;

  } catch {
    document.getElementById("results").innerHTML = "Erreur interaction";
  }
});

// 📊 FICHE
btnFiche.addEventListener("click", async () => {
  const val = input.value;

  if (!val) {
    alert("Entre une substance !");
    return;
  }

  try {
    const res = await fetch(${API}/fiche?nom=${encodeURIComponent(val)});
    const data = await res.json();

    document.getElementById("results").innerHTML = `
      <div class="card">
        <h3>Fiche complète</h3>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      </div>
    `;

  } catch {
    document.getElementById("results").innerHTML = "Erreur fiche";
  }
});