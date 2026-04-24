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

# 📂 Charger base
with open("data/database.json", encoding="utf-8") as f:
    DATABASE = json.load(f)

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()

    # 🔹 BASE LOCALE
    results = [x for x in DATABASE if nom in x["nom"].lower()]

    if results:
        return {"source": "local", "data": results}

    # 🔹 PUBCHEM
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

    # 🔹 IA
    try:
        prompt = f"Give toxicological and scientific data for {nom}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        result_clean = result.encode("ascii", "ignore").decode()

        return {"source": "ai", "data": result_clean}

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
# 🏠 ROOT
# -------------------------
# -------------------------
# 📊 FICHE COMPLETE
# -------------------------
@app.get("/fiche")
def fiche(nom: str):

    prompt = f"""
    Generate a FULL scientific toxicology report for {nom}.

    If plant:
    - botanical identification
    - chemical composition
    - description
    - pharmacological activities
    - toxicity (acute, chronic)
    - interactions
    - contraindications
    - side effects
    - indications
    - dosage
    - preparation
    - risk populations

    If drug:
    - ADME (absorption, distribution, metabolism, elimination)
    - half-life
    - LD50
    - therapeutic window
    - toxic dose
    - mechanisms of toxicity
    - target organs
    - symptoms
    - carcinogenicity / mutagenicity
    - antidotes
    - interactions
    - risk factors

    If chemical:
    - CAS number
    - hazard pictograms
    - exposure routes
    - acute toxicity
    - chronic toxicity
    - VLEP
    - PPE
    - storage
    - first aid
    - spill management
    - environmental impact

    Make it structured and clear.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # éviter bug accent
        clean = result.encode("ascii", "ignore").decode()

        return {"fiche": clean}

    except Exception as e:
        return {"error": str(e)}
# -------------------------
# 📊 FICHE COMPLETE
# -------------------------
@app.get("/fiche")
def fiche(nom: str):

    try:
        prompt = f"""
        Give a full scientific and toxicological report for {nom}.
        Include pharmacology, toxicity, risks, and recommendations.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # 🔥 éviter bug caractères
        clean = result.encode("ascii", "ignore").decode()

        return {"fiche": clean}

    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"} PRO OK"}