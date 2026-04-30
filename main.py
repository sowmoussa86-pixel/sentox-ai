from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from fpdf import FPDF
import os

app = FastAPI()

# =========================
# 🧪 BASE DE DONNÉES LOCALE
# =========================

database = [
    {
        "nom": "paracetamol",
        "type": "medicament",
        "description": "antalgique et antipyrétique",
        "toxicologie": "hepatotoxique en surdosage",
        "dose": "max 4g/jour"
    },
    {
        "nom": "aspirine",
        "type": "medicament",
        "description": "anti-inflammatoire",
        "toxicologie": "risque hemorragique",
        "dose": "500mg à 1g"
    },
    {
        "nom": "ibuprofene",
        "type": "medicament",
        "description": "anti-inflammatoire non stéroïdien",
        "toxicologie": "toxique pour l'estomac et reins",
        "dose": "200-400mg"
    },
    {
        "nom": "neem",
        "type": "plante",
        "description": "plante médicinale antiseptique et antiparasitaire",
        "toxicologie": "toxique à forte dose",
        "dose": "usage traditionnel modéré"
    },
    {
        "nom": "quinine",
        "type": "medicament",
        "description": "antipaludique",
        "toxicologie": "cinchonisme à forte dose",
        "dose": "selon prescription"
    }
]

# =========================
# 🔍 SEARCH
# =========================

@app.get("/search")
def search(nom: str):

    nom = nom.lower().strip()

    results = []

    for item in database:
        if (
            nom in item["nom"].lower()
            or nom in item["type"].lower()
            or nom in item["description"].lower()
        ):
            results.append(item)

    if results:
        return {"source": "local", "data": results}

    # 🔁 fallback PubChem
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nom}/property/MolecularFormula,MolecularWeight/JSON"
        r = requests.get(url)
        data = r.json()

        props = data["PropertyTable"]["Properties"][0]

        return {
            "source": "pubchem",
            "data": {
                "nom": nom,
                "formula": props.get("MolecularFormula"),
                "weight": props.get("MolecularWeight")
            }
        }

    except:
        return {"error": "Substance non trouvée"}

# =========================
# ⚠️ INTERACTION
# =========================

@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    if "paracetamol" in noms_list and "alcool" in noms_list:
        return {"danger": "⚠️ Risque hépatotoxique grave"}

    if "aspirine" in noms_list and "ibuprofene" in noms_list:
        return {"danger": "⚠️ Risque hémorragique augmenté"}

    return {"message": "Aucune interaction majeure connue"}

# =========================
# 🤖 IA TOXICOLOGIQUE SIMPLE
# =========================

@app.get("/ai/{nom}")
def analyse_ai(nom: str):

    nom = nom.lower()

    for item in database:
        if nom in item["nom"]:
            return {
                "analyse": f"{item['nom']} est {item['type']}.\n"
                           f"Effet: {item['description']}.\n"
                           f"Toxicologie: {item['toxicologie']}.\n"
                           f"Dose: {item['dose']}"
            }

    return {"analyse": "Aucune donnée IA disponible"}

# =========================
# 📄 PDF
# =========================

@app.get("/pdf/{nom}")
def generate_pdf(nom: str):

    nom = nom.lower()
    filename = f"{nom}.pdf"

    contenu = None

    for item in database:
        if nom in item["nom"]:
            contenu = item
            break

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="RAPPORT SENTOX", ln=True)

    if contenu:
        pdf.cell(200, 10, txt=f"Nom: {contenu['nom']}", ln=True)
        pdf.cell(200, 10, txt=f"Type: {contenu['type']}", ln=True)
        pdf.cell(200, 10, txt=f"Description: {contenu['description']}", ln=True)
        pdf.cell(200, 10, txt=f"Toxicologie: {contenu['toxicologie']}", ln=True)
        pdf.cell(200, 10, txt=f"Dose: {contenu['dose']}", ln=True)
    else:
        pdf.cell(200, 10, txt="Substance non trouvée", ln=True)

    pdf.output(filename)

    if os.path.exists(filename):
        return FileResponse(filename, media