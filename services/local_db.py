import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.json")

with open(DB_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

def get_all():
    return DATA

def search_local(name):
    results = []
    for item in DATA:
        if name.lower() in item["nom"].lower():
            results.append(item)
    return results