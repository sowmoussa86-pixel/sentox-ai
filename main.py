from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.local_db import search_local
from services.pubchem import search_pubchem

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SCORE TOXICO
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

# HOME
@app.get("/")
def home():
    return {"message": "SENTOX API OK"}

# SEARCH
@app.get("/search")
def search(nom: str):
    local_results = search_local(nom)
    pubchem_result = search_pubchem(nom)

    # ajouter score toxicologique
    for item in local_results:
        item["score_toxicologique"] = score_toxicologique(item.get("dl50"))

    return {
        "local": local_results,
        "scientifique": pubchem_result
    }