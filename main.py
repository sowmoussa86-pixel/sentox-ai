# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

import os
import requests

from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

# -------------------------
# 🔎 BASE LOCALE
# -------------------------
DATABASE = [
    {"id":1,"nom":"neem","dl50":5000,"type":"plante"},
    {"id":2,"nom":"paracetamol","dl50":338,"type":"medicament"},
    {"id":3,"nom":"methanol","dl50":5628,"type":"chimique"},
    {"id":4,"nom":"aspirine","dl50":200,"type":"medicament"}
]

# -------------------------
# 🧪 SCORE TOXICOLOGIQUE
# -------------------------
def compute_toxicity(dl50):
    if dl50 <= 50:
        return "Very toxic", "Liver / nervous system"
    elif dl50 <= 300:
        return "Toxic", "Liver / kidneys"
    elif dl50 <= 2000:
        return "Moderate", "Digestive system"
    else:
        return "Low", "No critical organ"

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()
    results = []

    # 🔹 1. BASE LOCALE
    for item in DATABASE:
        if nom in item["nom"]:
            results.append(item)

    # 🔹 2. SI TROUVÉ → RETOUR
    if results:
        return {
            "source": "local",
            "data": results
        }

    # 🔹 3. PUBCHEM (chimique)
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

    # 🔹 4. IA (ULTIME FALLBACK)
    try:
        prompt = f"""
        Give scientific, pharmacological and toxicological data for {nom}.
        Include:
        - type (plant, drug, chemical)
        - toxicity (DL50, NOAEL if possible)
        - pharmacology
        - risks
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        return {
            "source": "ai",
            "data": result
        }

    except:
        return {
            "error": "Substance non trouvée"
        }
    except:
        scientifique = None

    return {
        "local": results,
        "scientifique": scientifique,
        "suggestions": [x["nom"] for x in DATABASE if nom in x["nom"]]
    }

# -------------------------
# 🧠 IA CHATGPT (STABLE)
# -------------------------
@app.get("/ai")
def ai_analysis(nom: str):

    prompt = f"""
    Provide a toxicological analysis of {nom}.
    Include:
    - toxicity level
    - affected organs
    - risks
    - recommendations
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a toxicology expert"},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        # 🔥 FIX ASCII (évite crash Render)
        result_clean = result.encode("ascii", "ignore").decode()

        return JSONResponse(content={"result": result_clean})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# -------------------------
# ⚗️ INTERACTION
# -------------------------
@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    # ⚠️ règle simple
    if "paracetamol" in noms_list and "methanol" in noms_list:
        interaction_msg = "High hepatotoxic risk"
    else:
        interaction_msg = "No major interaction known"

    result = []

    for n in noms_list:
        try:
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{n}/JSON"
            requests.get(url)
            info = "PubChem data available"
        except:
            info = "No data"

        result.append({"nom": n, "info": info})

    return {
        "substances": noms_list,
        "interaction": interaction_msg,
        "details": result
    }

# -------------------------
# 📄 PDF
# -------------------------
@app.get("/export")
def export(nom: str):

    results = search(nom)["local"]

    file_path = "rapport.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    for item in results:
        text = f"{item['nom']} - DL50: {item['dl50']} - Danger: {item['danger']}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return FileResponse(file_path, filename="sentox_report.pdf")

# -------------------------
# 🏠 ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}