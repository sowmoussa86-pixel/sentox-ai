import json

with open("data/database.json", encoding="utf-8") as f:
    DATA = json.load(f)

def search_local(name):
    results = []
    for item in DATA:
        if name.lower() in item["nom"].lower():
            results.append(item)
    return results