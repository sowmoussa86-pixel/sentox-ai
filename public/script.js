const API = "https://sentox-ai-backend.onrender.com";

window.onload = () => {

  const input = document.getElementById("searchInput");
  const resultDiv = document.getElementById("results");

  const btnSearch = document.getElementById("btnSearch");
  const btnInteraction = document.getElementById("btnInteraction");
  const btnFiche = document.getElementById("btnFiche");

  // 🔍 RECHERCHE
  btnSearch.onclick = async () => {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(${API}/search?nom=${val});
      const data = await res.json();
      resultDiv.innerHTML = <pre>${JSON.stringify(data, null, 2)}</pre>;
    } catch {
      resultDiv.innerHTML = "Erreur serveur";
    }
  };

  // ⚗️ INTERACTION
  btnInteraction.onclick = async () => {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(${API}/interaction?nom=${val});
      const data = await res.json();
      resultDiv.innerHTML = <pre>${JSON.stringify(data, null, 2)}</pre>;
    } catch {
      resultDiv.innerHTML = "Erreur interaction";
    }
  };

  // 📊 FICHE
  btnFiche.onclick = async () => {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(${API}/fiche?nom=${val});
      const data = await res.json();
      resultDiv.innerHTML = <pre>${JSON.stringify(data, null, 2)}</pre>;
    } catch {
      resultDiv.innerHTML = "Erreur fiche";
    }
  };

};