from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS (obligatoire pour le site web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger base de données
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "database.json")

with open(file_path, encoding="utf-8") as f:
    DATA = json.load(f)
    DATA = json.load(f)
    DATA = json.load(f)

# SCORE TOXICOLOGIQUE
def score_toxicologique(dl50):
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

# GET ALL
@app.get("/substances")
def get_all():
    result = []
    for item in DATA:
        item_copy = item.copy()
        item_copy["score_toxicologique"] = score_toxicologique(item.get("dl50", 1000))
        result.append(item_copy)
    return result

# SEARCH
@app.get("/search")
def search(nom: str):
    results = []
    for item in DATA:
        if nom.lower() in item["nom"].lower():
            item_copy = item.copy()
            item_copy["score_toxicologique"] = score_toxicologique(item.get("dl50", 1000))
            results.append(item_copy)
    return results

# INTERACTION SIMPLE
def check_interaction(item1, item2):
    interactions = []

    if item1["id"] == item2["id"]:
        return ["Même substance"]

    if item1["nom"] == "Paracétamol" and item2["nom"] == "Methanol":
        interactions.append("⚠️ Risque hépatotoxique grave")

    if item2["nom"] == "Paracétamol" and item1["nom"] == "Methanol":
        interactions.append("⚠️ Risque hépatotoxique grave")

    if not interactions:
        return ["Aucune interaction connue"]

    return interactions

# INTERACTION MULTI
@app.get("/interaction-multi")
def interaction_multi(ids: str):
    id_list = [int(x) for x in ids.split(",")]

    items = [x for x in DATA if x["id"] in id_list]

    interactions = []

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            inter = check_interaction(items[i], items[j])
            interactions.extend(inter)

    interactions = list(set(interactions))

    return {
        "substances": [item["nom"] for item in items],
        "interactions": interactions
    }