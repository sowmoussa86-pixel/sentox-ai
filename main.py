from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fpdf import FPDF

app = FastAPI()

# ✅ autorise le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE SIMPLE
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
        return {"data": results}

    return {"error": "Non trouvé"}

# =========================
# INTERACTION
# =========================
@app.get("/interaction")
def interaction(noms: str):
    return {
        "substances": noms,
        "risque": "Interaction possible",
        "conseil": "Consulter un expert"
    }

# =========================
# IA
# =========================
@app.get("/ai")
def ai(nom: str):
    return {
        "substance": nom,
        "analyse": "Analyse IA : risque dépend de la dose, surveiller foie"
    }

# =========================
# PDF
# =========================
@app.get("/pdf/{nom}")
def pdf(nom: str):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="RAPPORT TOXICOLOGIQUE SENTOX", ln=True)
    pdf.cell(200, 10, txt=f"Substance: {nom}", ln=True)
    pdf.cell(200, 10, txt="Analyse: risque dépend de la dose", ln=True)

    filename = f"{nom}.pdf"
    pdf.output(filename)

    return FileResponse(filename, media_type="application/pdf", filename=filename)