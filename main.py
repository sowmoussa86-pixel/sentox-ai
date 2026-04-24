# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
with open("data/database.json", encoding="utf-8") as f:
    DATABASE = json.load(f)

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()

    results = [x for x in DATABASE if nom in x["nom"].lower()]

    if results:
        return JSONResponse(content={"source": "local", "data": results})

    # PubChem fallback
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nom}/property/MolecularFormula,MolecularWeight/JSON"
        r = requests.get(url)
        data = r.json()

        props = data["PropertyTable"]["Properties"][0]

        return JSONResponse(content={
            "source": "pubchem",
            "data": {
                "nom": nom,
                "formula": props.get("MolecularFormula"),
                "weight": props.get("MolecularWeight")
            }
        })
    except:
        return JSONResponse(content={"error": "Substance not found"})

# -------------------------
# ⚗️ INTERACTION
# -------------------------
@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    if "paracetamol" in noms_list and "alcohol" in noms_list:
        return JSONResponse(content={"result": "High liver toxicity risk"})

    if "warfarin" in noms_list and "aspirin" in noms_list:
        return JSONResponse(content={"result": "High bleeding risk"})

    if "benzene" in noms_list:
        return JSONResponse(content={"result": "Chronic toxicity (bone marrow)"})

    return JSONResponse(content={"result": "No major interaction"})

# -------------------------
# 📊 FICHE COMPLETE (SANS IA)
# -------------------------
@app.get("/fiche")
def fiche(nom: str):

    nom = nom.lower()

    if "paracetamol" in nom:
        return JSONResponse(content={
            "fiche": """
Substance: Paracetamol

Type: Medicament

Pharmacology:
- Analgesic
- Antipyretic

Toxicity:
- Hepatotoxic in overdose

Target organ:
- Liver

Symptoms:
- Nausea
- Vomiting
- Liver failure

Recommendation:
- Respect dosage
- Avoid alcohol
"""
        })

    if "benzene" in nom:
        return JSONResponse(content={
            "fiche": """
Substance: Benzene

Type: Chemical

Toxicity:
- Carcinogenic
- Chronic exposure dangerous

Target:
- Bone marrow

Exposure:
- Inhalation

Precaution:
- Use protective equipment
"""
        })

    return JSONResponse(content={
        "fiche": f"No detailed data available for {nom}"
    })

# -------------------------
# ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}