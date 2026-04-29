const API = "https://sentox-ai-backend.onrender.com"; // ⚠️ ton backend

function search() {
    const value = document.getElementById("input").value;

    fetch(${API}/search?nom=${value})
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    });
}

function interaction() {
    const value = document.getElementById("input").value;

    fetch(${API}/interaction?noms=${value})
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    });
}

function pdf() {
    const value = document.getElementById("input").value;

    window.open(${API}/pdf/${value}, "_blank");
}

function ai() {
    const value = document.getElementById("input").value;

    fetch(${API}/ai?nom=${value})
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    });
}