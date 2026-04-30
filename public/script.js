// 🔍 RECHERCHE
async function rechercher() {
    let nom = document.getElementById("search").value;

    if (!nom) {
        alert("Entrer une substance");
        return;
    }

    try {
        let res = await fetch(/search?nom=${nom});
        let data = await res.json();

        let div = document.getElementById("resultat");

        if (!data.data || data.data.length === 0) {
            div.innerHTML = "Aucun résultat";
            return;
        }

        let item = data.data[0];

        div.innerHTML = `
            <h2>${item.nom}</h2>
            <p><b>Type :</b> ${item.type}</p>
            <p><b>Description :</b> ${item.description || "-"}</p>
            <p><b>Toxicologie :</b> ${item.toxicologie || "-"}</p>
        `;

    } catch (error) {
        document.getElementById("resultat").innerHTML = "Erreur serveur";
    }
}


// ⚡ INTERACTION
async function interaction() {
    let nom = document.getElementById("search").value;

    if (!nom) {
        alert("Entrer une substance");
        return;
    }

    try {
        let res = await fetch(/interaction?noms=${nom});
        let data = await res.json();

        document.getElementById("resultat").innerHTML =
            "<b>Interaction :</b><br>" + JSON.stringify(data);

    } catch (error) {
        document.getElementById("resultat").innerHTML = "Erreur interaction";
    }
}


// 📄 PDF
function pdf() {
    let nom = document.getElementById("search").value;

    if (!nom) {
        alert("Entrer une substance");
        return;
    }

    window.open(/pdf?nom=${nom}, "_blank");
}


// 🤖 IA
async function analyseIA() {
    let nom = document.getElementById("search").value;

    if (!nom) {
        alert("Entrer une substance");
        return;
    }

    try {
        let res = await fetch(/ai?nom=${nom});
        let data = await res.json();

        document.getElementById("resultat").innerHTML =
            "<b>Analyse IA :</b><br>" + (data.analyse || "Aucune analyse");

    } catch (error) {
        document.getElementById("resultat").innerHTML = "Erreur IA";
    }
}