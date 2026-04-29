from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fpdf import FPDF
import requests

app = FastAPI()

# ✅ Autoriser le frontend (important sinon boutons bloqués)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# BASE DE DONNÉES SIMPLE
# =========================
database = [
    {
        "nom": "paracetamol",
        "type": "medicament",
        "description": "Antalgique et antipyrétique",
        "toxicologie": "Hépatotoxique à forte dose"
    },
    {
        "nom": "neem",
        "type": "plante",
        "description": "Plante médicinale utilisée en Afrique et en Inde",
        "toxicologie": "Faible à dose normale, toxique à forte dose"
    }
]

# =========================
# SEARCH
# =========================
@app.get("/search")
def search(nom: str):
    nom = nom.lower()

    results = [x for x in database if nom in x["nom"]]

    if results:
        return {"source": "local", "data": results}

    return {"error": "Substance non trouvée"}

# =========================
# INTERACTION
# =========================
@app.get("/interaction")
def interaction(noms: str):
    noms_list = [x.strip().lower() for x in noms.split(",")]

    return {
        "substances": noms_list,
        "risque": "Interaction modérée possible",
        "conseil": "Consulter un spécialiste"
    }

# =========================
# IA ANALYSE
# =========================
@app.get("/ai")
def analyse_ai(nom: str):
    return {
        "substance": nom,
        "niveau_risque": "modéré",
        "analyse": "Analyse IA : effet possible sur le foie, dépend de la dose"
    }

# =========================
# PDF
# =========================
@app.get("/pdf/{nom}")
def generate_pdf(nom: str):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="RAPPORT TOXICOLOGIQUE SENTOX", ln=True)
    pdf.cell(200, 10, txt=f"Substance: {nom}", ln=True)
    pdf.cell(200, 10, txt="Analyse: Risque dépend de la dose", ln=True)

    file_name = f"{nom}.pdf"
    pdf.output(file_name)

    return FileResponse(file_name, media_type='application/pdf', filename=file_name)