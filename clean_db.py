import json
import re

# lire fichier brut
with open("data/database.json", encoding="utf-8") as f:
    raw = f.read()

# extraire tous les objets {...}
matches = re.findall(r'\{[^{}]*\}', raw)

clean = []
seen = set()

for m in matches:
    try:
        item = json.loads(m)

        nom = item.get("nom", "").lower().strip()

        if not nom:
            continue

        if nom in seen:
            continue

        seen.add(nom)

        item["nom"] = nom
        item["type"] = item.get("type", "inconnu")

        clean.append(item)

    except:
        continue

# sauvegarde
with open("data/database_clean.json", "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=2, ensure_ascii=False)

print(f"✅ OK : {len(clean)} produits nettoyés")