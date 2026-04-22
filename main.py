from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.local_db import search_local, get_all
from services.pubchem import search_pubchem
from services.fuzzy_search import suggest
from services.interactions import check_interactions

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}

# 🔎 RECHERCHE COMPLETE
@app.get("/search")
def search(nom: str):
    local_results = search_local(nom)
    pubchem_result = search_pubchem(nom)
    suggestions = suggest(nom, get_all())

    return {
        "local": local_results,
        "scientifique": pubchem_result,
        "suggestions": suggestions
    }

# ⚗️ INTERACTIONS
@app.get("/interaction")
def interaction(ids: str):
    id_list = [int(x) for x in ids.split(",")]
    data = get_all()
    items = [x for x in data if x["id"] in id_list]

    return {
        "substances": [x["nom"] for x in items],
        "interactions": check_interactions(items)
    }

# 📄 EXPORT PDF
@app.get("/export")
def export(nom: str):
    results = search_local(nom)

    doc = SimpleDocTemplate("rapport.pdf")
    styles = getSampleStyleSheet()

    content = []

    for item in results:
        text = f"{item['nom']} - DL50: {item['dl50']} - Danger: {item['danger']}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return {"message": "PDF généré"}