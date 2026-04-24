# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
import requests
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 Charger base locale
with open("data/database.json", encoding="utf-8") as f:
    DATABASE = json.load(f)

# -------------------------
# 🔎 SEARCH FINAL
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()
    results = []

    # 🔹 1. BASE LOCALE
    for item in DATABASE:
        if nom in item["nom"].lower():
            results.append(item)

    if results:
        return {"source": "local", "data": results}

    # 🔹 2. PUBCHEM
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

    # 🔹 3. IA
    try:
        prompt = f"""
        Give scientific, pharmacological and toxicological data for {nom}.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        return {"source": "ai", "data": result}

    except:
        return {"error": "Substance non trouvée"}

# -------------------------
# 🏠 ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}