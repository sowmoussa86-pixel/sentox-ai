import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.json")

with open(DB_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

# 🔥 enrichissement automatique
def enrich_data(item):
    dl50 = item.get("dl50", 1000)

    if dl50 <= 50:
        item["danger"] = "🔴 élevé"
        item["organe"] = "foie"
    elif dl50 <= 300:
        item["danger"] = "🟠 modéré"
        item["organe"] = "rein"
    else:
        item["danger"] = "🟢 faible"
        item["organe"] = "aucun critique"

    return item

def get_all():
    return [enrich_data(x.copy()) for x in DATA]

def search_local(name):
    results = []
    for item in DATA:
        if name.lower() in item["nom"].lower():
            results.append(enrich_data(item.copy()))
    return results