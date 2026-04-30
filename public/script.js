const API = "https://sentox-ai-backend.onrender.com";

function search() {
    const value = document.getElementById("input").value;

    fetch(API + "/search?nom=" + value)
    .then(res => res.json())
    .then(data => {

        if (data.data) {
            const item = data.data[0];

            document.getElementById("result").innerHTML = `
                <h3>${item.nom}</h3>
                <p><b>Type:</b> ${item.type}</p>
                <p><b>Description:</b> ${item.description}</p>
                <p><b>Toxicologie:</b> ${item.toxicologie}</p>
            `;
        } else {
            document.getElementById("result").innerHTML = "Aucun résultat";
        }

    });
}

function interaction() {
    const value = document.getElementById("input").value;

    fetch(API + "/interaction?noms=" + value)
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            JSON.stringify(data);
    });
}

function pdf() {
    const value = document.getElementById("input").value;
    window.open(API + "/pdf/" + value);
}

function ai() {
    const value = document.getElementById("input").value;

    fetch(API + "/ai?nom=" + value)
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "<b>Analyse IA:</b> " + data.analyse;
    });
}