const API = "https://sentox-ai-backend.onrender.com";

window.onload = function () {

  alert("JS connecté"); // 👈 doit apparaître

  const input = document.getElementById("searchInput");
  const result = document.getElementById("results");

  document.getElementById("btnSearch").onclick = async function () {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(API + "/search?nom=" + val);
      const data = await res.json();
      result.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    } catch {
      result.innerHTML = "Erreur recherche";
    }
  };

  document.getElementById("btnInteraction").onclick = async function () {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(API + "/interaction?nom=" + val);
      const data = await res.json();
      result.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    } catch {
      result.innerHTML = "Erreur interaction";
    }
  };

  document.getElementById("btnFiche").onclick = async function () {
    const val = input.value.trim();
    if (!val) return alert("Entre une substance");

    try {
      const res = await fetch(API + "/fiche?nom=" + val);
      const data = await res.json();
      result.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    } catch {
      result.innerHTML = "Erreur fiche";
    }
  };

};