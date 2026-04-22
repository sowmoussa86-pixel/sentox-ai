from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

def score_toxicologique(dl50):
    try:
        dl50 = float(dl50)
    except:
        return "Inconnu"

    if dl50 <= 50:
        return "🔴 Très toxique"
    elif dl50 <= 300:
        return "🟠 Toxique"
    elif dl50 <= 2000:
        return "🟡 Modéré"
    else:
        return "🟢 Faible"

@app.get("/")
def home():
    return {"message": "SENTOX API PRO OK"}

@app.get("/search")
def search(nom: str):
    local_results = search_local(nom)
    pubchem_result = search_pubchem(nom)
    suggestions = suggest(nom, get_all())

    for item in local_results:
        item["score_toxicologique"] = score_toxicologique(item["dl50"])

    return {
        "local": local_results,
        "scientifique": pubchem_result,
        "suggestions": suggestions
    }

@app.get("/interaction")
def interaction(ids: str):
    id_list = [int(x) for x in ids.split(",")]
    data = get_all()
    items = [x for x in data if x["id"] in id_list]

    return {
        "substances": [x["nom"] for x in items],
        "interactions": check_interactions(items)
    }