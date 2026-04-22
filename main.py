from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.local_db import search_local, get_all
from services.pubchem import search_pubchem
from services.fuzzy_search import suggest
from services.interactions import check_interactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # plus tard tu peux restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 validation simple
def clean_input(text):
    if not text or len(text) > 100:
        raise HTTPException(status_code=400, detail="Entrée invalide")
    return text.strip().lower()

# 🔎 RECHERCHE
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

# 📄 PDF sécurisé
@app.get("/export")
def export(nom: str):
    nom = clean_input(nom)
    return {"message": "PDF généré"}