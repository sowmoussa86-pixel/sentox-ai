from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

import os
import requests
import unicodedata

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
# 🔎 BASE LOCALE SIMPLE
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
        return "🔴 Très toxique", "Foie / système nerveux"
    elif dl50 <= 300:
        return "🟠 Toxique", "Foie / reins"
    elif dl50 <= 2000:
        return "🟡 Modéré", "Digestif"
    else:
        return "🟢 Faible", "Aucun critique"

# -------------------------
# 🔎 SEARCH
# -------------------------
@app.get("/search")
def search(nom: str):

    nom = nom.lower()

    results = []

    for item in DATABASE:
        if nom in item["nom"]:
            danger, organe = compute_toxicity(item["dl50"])

            item_copy = item.copy()
            item_copy["danger"] = danger
            item_copy["organe"] = organe

            results.append(item_copy)

    # 🌍 PUBCHEM
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nom}/property/MolecularFormula,MolecularWeight/JSON"
        r = requests.get(url)
        data = r.json()

        props = data["PropertyTable"]["Properties"][0]

        scientifique = {
            "formula": props.get("MolecularFormula"),
            "poids": props.get("MolecularWeight")
        }
    except:
        scientifique = None

    return {
        "local": results,
        "scientifique": scientifique,
        "suggestions": [x["nom"] for x in DATABASE if nom in x["nom"]]
    }

from fastapi.responses import JSONResponse

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

        # 🔥 FIX FINAL : enlever tous les caractères non ASCII
        result_clean = result.encode("ascii", "ignore").decode()

        return JSONResponse(content={"result": result_clean})

    except Exception as e:
        return {"error": str(e)}

        result = response.choices[0].message.content

        return JSONResponse(content={"result": result})

    except Exception as e:
        return {"error": str(e)}
# -------------------------
# ⚗️ INTERACTION
# -------------------------
@app.get("/interaction")
def interaction(noms: str):

    noms_list = [x.strip().lower() for x in noms.split(",")]

    result = []

    # ⚠️ règles simples (extensible)
    if "paracetamol" in noms_list and "methanol" in noms_list:
        interaction_msg = "⚠️ Risque hepatotoxique eleve"
    else:
        interaction_msg = "Aucune interaction majeure connue"

    # 🌍 PubChem (placeholder scientifique)
    for n in noms_list:
        try:
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{n}/JSON"
            r = requests.get(url)
            data = r.json()

            info = "Donnees PubChem disponibles"
        except:
            info = "Pas de donnees"

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

    return FileResponse(file_path, filename="rapport_sentox.pdf")

# -------------------------
# 🏠 ROOT
# -------------------------
@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}