from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from openai import OpenAI

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

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    return {
        "local": search_local(nom),
        "scientifique": search_pubchem(nom),
        "suggestions": suggest(nom, get_all())
    }

# 🧠 IA CHATGPT
@app.get("/ai")
def ai_analysis(nom: str):
    nom = clean_input(nom)

    prompt = f"""
    Donne une analyse toxicologique simple pour : {nom}
    - toxicité
    - organes affectés
    - risques
    - recommandations
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"result": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}

# ⚗️ INTERACTION
@app.get("/interaction")
def interaction(ids: str):
    id_list = [int(x) for x in ids.split(",")]
    data = get_all()
    items = [x for x in data if x["id"] in id_list]

    return {
        "substances": [x["nom"] for x in items],
        "interactions": check_interactions(items)
    }

# 📄 PDF
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
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/ai")
def ai_analysis(nom: str):

    prompt = f"""
    Analyse toxicologique de {nom}.
    Donne :
    - toxicité
    - organes affectés
    - risques
    - recommandations
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en toxicologie"},
                {"role": "user", "content": prompt}
            ]
        )

        return {"result": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}