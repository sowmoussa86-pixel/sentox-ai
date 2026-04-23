# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "SENTOX PRO OK"}

# 🔎 TEST SEARCH SIMPLE
@app.get("/search")
def search(nom: str):
    return {
        "local":[{"nom": nom, "dl50": 500, "danger":"🟡 modéré", "organe":"foie"}],
        "scientifique": None,
        "suggestions":[nom]
    }

# 🧠 IA CHATGPT
from fastapi.responses import JSONResponse
import unicodedata

@app.get("/ai")
def ai_analysis(nom: str):

    prompt = f"Analyse toxicologique de {nom}. Donner toxicite, organes affectes, risques et recommandations."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a toxicology expert"},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        # 🔥 SUPPRIMER LES ACCENTS (clé du problème)
        result_clean = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore').decode('ascii')

        return JSONResponse(content={"result": result_clean})

    except Exception as e:
        return {"error": str(e)}