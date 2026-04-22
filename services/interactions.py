def check_interactions(items):
    noms = [x["nom"].lower() for x in items]

    interactions = []

    if "paracetamol" in noms and "methanol" in noms:
        interactions.append("⚠️ Risque hépatotoxique grave")

    if "aspirine" in noms and "ibuprofen" in noms:
        interactions.append("⚠️ Risque digestif")

    if not interactions:
        interactions.append("✅ Aucune interaction connue")

    return interactions