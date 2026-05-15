async function rechercher() {
    let res = await fetch(`/search/${nom}`);
    let data = await res.json();

    if (data.error) {
        document.getElementById("resultat").innerHTML = data.error;
        return;
    }

    document.getElementById("resultat").innerHTML = `
        <h2>${data.Nom}</h2>
        <p><b>Formule :</b> ${data.Formule}</p>
        <p><b>Poids moléculaire :</b> ${data["Poids moléculaire"]}</p>
        <p><b>Nom IUPAC :</b> ${data["Nom IUPAC"]}</p>
    `;
}

async function analyseIA() {

    let nom = document.getElementById("search").value;

    let res = await fetch(`/analyse/${nom}`);
    let data = await res.json();

    if (data.error) {
        document.getElementById("resultat").innerHTML = `
            <h2>Erreur IA</h2>
            <p>${data.error}</p>
        `;

        return;
    }

    document.getElementById("resultat").innerHTML = `
        <h2>Analyse IA SENTOX</h2>

        <p><b>Produit :</b> ${data.Produit}</p>

        <pre style="
        white-space: pre-wrap;
        font-family: Arial;
        line-height: 1.5;
        ">
${data["Analyse IA"]}
        </pre>
    `;
}

async function interaction() {

    let nom = document.getElementById("search").value;

    let res = await fetch(`/interaction/${nom}`);
    let data = await res.json();

    document.getElementById("resultat").innerHTML = `
        <h2>Interactions</h2>
        <p><b>Produit :</b> ${data.Produit}</p>
        <ul>
            ${data["Interactions possibles"].map(i => `<li>${i}</li>`).join("")}
        </ul>
    `;
}

function pdf() {

    let nom = document.getElementById("search").value;

    window.open(`/pdf/${nom}`, "_blank");
}