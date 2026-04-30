from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from fpdf import FPDF
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📚 BASE DE DONNÉES LOCALE
# =========================
DATABASE = [
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
        "dose": "500mg"
    },
    {
        "nom": "neem",
        "type": "plante",
        "description": "plante médicinale africaine",
        "toxicologie": "toxique à forte dose",
        "dose": "usage modéré"
    }
]

# =========================
# 🔍 SEARCH (LOCAL + PUBCHEM)
# =========================
@app.get("/search")
def search(nom: str):

    nom = nom.lower().strip()

    results = []

    for item in DATABASE:
        if (
            nom in item["nom"].lower()
            or nom in item["description"].lower()
            or nom in item["type"].lower()
        ):
            results.append(item)

    if results:
        return {"source": "local", "data": results}

    # fallback PubChem
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nom}/property/MolecularFormula,MolecularWeight/JSON"
        r = requests.get(url, timeout=5)
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
        return {"danger": "⚠️ Risque hépatotoxique"}

    if "aspirine" in noms_list and "ibuprofene" in noms_list:
        return {"danger": "⚠️ Risque hémorragique"}

    return {"message": "Aucune interaction majeure"}

# =========================
# 🤖 IA SIMPLE (STABLE)
# =========================
@app.get("/ai")
def analyse_ai(nom: str):

    nom = nom.lower()

    for item in DATABASE:
        if nom in item["nom"]:
            return {
                "analyse": f"{item['nom']} → {item['toxicologie']}. Dose: {item['dose']}"
            }

    return {"analyse": "Aucune donnée IA disponible"}

# =========================
# 📄 PDF ROBUSTE
# =========================
@app.get("/pdf/{nom}")
def generate_pdf(nom: str):

    nom = nom.lower()
    filename = f"{nom}.pdf"

    produit = None
    for item in DATABASE:
        if nom in item["nom"]:
            produit = item
            break

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="RAPPORT SENTOX", ln=True)

    if produit:
        pdf.cell(200, 10, txt=f"Nom: {produit['nom']}", ln=True)
        pdf.cell(200, 10, txt=f"Type: {produit['type']}", ln=True)
        pdf.cell(200, 10, txt=f"Toxicologie: {produit['toxicologie']}", ln=True)
        pdf.cell(200, 10, txt=f"Dose: {produit['dose']}", ln=True)
    else:
        pdf.cell(200, 10, txt="Produit non trouvé", ln=True)

    pdf.output(filename)

    if os.path.exists(filename):
        return FileResponse(filename, media_type="application/pdf", filename=filename)

    return {"error": "PDF non généré"}

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "SENTOX API OK"}