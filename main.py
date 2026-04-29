# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import requests

app = FastAPI()

# ✅ Charger la base propre UNIQUEMENT
with open("data/database_clean.json", encoding="utf-8") as f:
    database = json.load(f)

print("Produits chargés :", len(database))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()

    results = [x for x in database if nom in x["nom"]]

    if results:
        return {"source": "local", "data": results}

    # PubChem fallback
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nom}/property/MolecularFormula,MolecularWeight/JSON"
        r = requests.get(url)
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
        return {"error": "Substance not found"}

@app.get("/ai")
def analyse_ai(nom: str):
    
    nom = nom.lower()

    if "paracetamol" in nom:
        return {
            "substance": "Paracétamol",
            "toxicite": "Hépatotoxique",
            "dose_dangereuse": "> 4g/jour",
            "niveau_risque": "⚠️ Modéré à élevé",
            "analyse": "Risque d’atteinte du foie en cas de surdosage"
        }

    elif "neem" in nom:
        return {
            "substance": "Neem",
            "toxicite": "Faible à dose normale",
            "niveau_risque": "⚠️ Faible",
            "analyse": "Peut devenir toxique à forte dose"
        }

    return {
        "substance": nom,
        "analyse": "Aucune donnée IA disponible",
        "niveau_risque": "❓ Inconnu"
    }
# -------------------------
# ⚗️ INTERACTION
# -------------------------
@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    if "paracetamol" in noms_list and "alcohol" in noms_list:
        return {"result": "High liver toxicity risk"}

    if "warfarin" in noms_list and "aspirin" in noms_list:
        return {"result": "High bleeding risk"}

    if "benzene" in noms_list:
        return {"result": "Chronic toxicity (bone marrow)"}

    return {"result": "No major interaction"}


# -------------------------
# 📊 FICHE COMPLETE (PROPRE)
# -------------------------
@app.get("/fiche")
def fiche(nom: str):

    nom = nom.lower()

    for item in database:
        if item["nom"].lower() == nom:

            fiche_text = f"""
Substance: {item.get('nom','-')}

Type: {item.get('type','-')}

Description:
{item.get('description','-')}

Pharmacologie:
{', '.join(item.get('pharmacologie', [])) if isinstance(item.get('pharmacologie'), list) else item.get('pharmacologie','-')}

Toxicité:
{item.get('toxicologie','-')}

Organes cibles:
{item.get('organes','-')}

Indications:
{', '.join(item.get('indications', [])) if isinstance(item.get('indications'), list) else item.get('indications','-')}

Posologie:
{item.get('posologie','-')}

Effets indésirables:
{', '.join(item.get('effets', [])) if isinstance(item.get('effets'), list) else item.get('effets','-')}
"""

            return {"fiche": fiche_text}

    return {"fiche": f"Aucune fiche disponible pour {nom}"}
# -------------------------
# ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}