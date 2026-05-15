from flask import Flask, jsonify, send_from_directory
import google.generativeai as genai
import requests
import os

app = Flask(__name__, static_folder="public")

# =========================
# CONFIGURATION GEMINI
# =========================

GEMINI_API_KEY = "GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# PAGE PRINCIPALE
# =========================

@app.route("/")
def home():
    return send_from_directory("public", "index.html")

# =========================
# FICHIERS STATIQUES
# =========================

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("public", path)

# =========================
# RECHERCHE PUBCHEM
# =========================

@app.route("/search/<query>")
def search(query):

    try:

        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{query}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"

        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({
                "error": "Produit non trouvé"
            })

        data = response.json()

        props = data["PropertyTable"]["Properties"][0]

        result = {
            "Nom": query,
            "Formule": props.get("MolecularFormula"),
            "Poids moléculaire": props.get("MolecularWeight"),
            "Nom IUPAC": props.get("IUPACName")
        }

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# ANALYSE IA GEMINI
# =========================

@app.route("/analyse/<query>")
def analyse(query):

    prompt = f"""
    Fais une analyse toxicologique scientifique du produit suivant :

    {query}

    Donne :
    - les risques toxicologiques
    - les organes cibles
    - les interactions possibles
    - les précautions
    - les recommandations scientifiques
    - un résumé clair
    """

    try:

        response = model.generate_content(prompt)

        texte = response.text

        return jsonify({
            "Produit": query,
            "Analyse IA": texte
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# INTERACTIONS
# =========================

@app.route("/interaction/<query>")
def interaction(query):

    result = {
        "Produit": query,
        "Interactions possibles": [
            "Interaction hépatique",
            "Interaction enzymatique",
            "Risque métabolique"
        ]
    }

    return jsonify(result)

# =========================
# PDF
# =========================

@app.route("/pdf/<query>")
def pdf(query):

    return jsonify({
        "message": f"PDF généré pour {query}"
    })

# =========================
# SERVEUR
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=8000)