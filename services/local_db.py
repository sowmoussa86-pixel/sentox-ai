import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.json")

with open(DB_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

def enrich_data(item):
    dl50 = item.get("dl50", 1000)

    if dl50 <= 50:
        danger = "🔴 Très toxique"
        organe = "Foie / système nerveux"
    elif dl50 <= 300:
        danger = "🟠 Toxique"
        organe = "Reins / foie"
    elif dl50 <= 2000:
        danger = "🟡 Modéré"
        organe = "Digestif"
    else:
        danger = "🟢 Faible"
        organe = "Aucun critique"

    item["danger"] = danger
    item["organe"] = organe

    # 🧠 ajout scientifique
    item["toxicologie"] = {
        "dl50": dl50,
        "classe": danger,
        "voie_exposition": "orale",
        "effets": "dose dépendante",
    }

    return item

def get_all():
    return [enrich_data(x.copy()) for x in DATA]

def search_local(name):
    results = []
    for item in DATA:
        if name.lower() in item["nom"].lower():
            results.append(enrich_data(item.copy()))
    return results