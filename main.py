# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import requests
from openai import OpenAI

app = FastAPI()

# 🔐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 DATABASE
with open("data/database.json", encoding="utf-8") as f:
    DATABASE = json.load(f)

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()

    # 🔹 base locale
    results = [x for x in DATABASE if nom in x["nom"].lower()]

    if results:
        return {"source": "local", "data": results}

    # 🔹 PubChem
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
        pass

    # 🔹 IA fallback
    try:
        prompt = f"Give scientific and toxicological data for {nom}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # éviter bug accents
        clean = result.encode("ascii", "ignore").decode()

        return {"source": "ai", "data": clean}

    except:
        return {"error": "Substance non trouvée"}

# -------------------------
# ⚗️ INTERACTION
# -------------------------
@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    if "paracetamol" in noms_list and "alcohol" in noms_list:
        return {"result": "High risk of liver toxicity"}

    if "warfarin" in noms_list and "aspirin" in noms_list:
        return {"result": "High bleeding risk"}

    if "benzene" in noms_list:
        return {"result": "Chronic toxicity (bone marrow)"}

    return {"result": "No major interaction known"}

# -------------------------
# 📊 FICHE COMPLETE
# -------------------------
@app.get("/fiche")
def fiche(nom: str):

    try:
        prompt = f"""
        Generate a full scientific toxicological report for {nom}.

        Include:
        - pharmacology
        - toxicity (acute, chronic)
        - risks
        - organs affected
        - interactions
        - recommendations
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # éviter erreur ASCII
        clean = result.encode("ascii", "ignore").decode()

        return {"fiche": clean}

    except Exception as e:
        return {"error": str(e)}

# -------------------------
# 🏠 ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}