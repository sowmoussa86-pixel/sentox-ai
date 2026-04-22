from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from services.local_db import search_local, get_all
from services.pubchem import search_pubchem
from services.fuzzy_search import suggest
from services.interactions import check_interactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_input(text):
    if not text or len(text) > 100:
        raise HTTPException(status_code=400, detail="Entrée invalide")
    return text.strip().lower()

@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}

# 🔎 SEARCH
@app.get("/search")
def search(nom: str):
    nom = clean_input(nom)

    local_results = search_local(nom)
    pubchem_result = search_pubchem(nom)
    suggestions = suggest(nom, get_all())

    return {
        "local": local_results,
        "scientifique": pubchem_result,
        "suggestions": suggestions
    }

# ⚗️ INTERACTION
@app.get("/interaction")
def interaction(ids: str):
    try:
        id_list = [int(x) for x in ids.split(",")]
    except:
        raise HTTPException(status_code=400, detail="IDs invalides")

    data = get_all()
    items = [x for x in data if x["id"] in id_list]

    return {
        "substances": [x["nom"] for x in items],
        "interactions": check_interactions(items)
    }

# 📄 PDF TELECHARGEABLE
@app.get("/export")
def export(nom: str):
    nom = clean_input(nom)

    results = search_local(nom)

    file_path = "rapport.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    for item in results:
        text = f"{item['nom']} - DL50: {item['dl50']} - Danger: {item['danger']}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return FileResponse(file_path, filename="rapport_sentox.pdf")