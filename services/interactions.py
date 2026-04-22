def check_interactions(items):
    interactions = []

    noms = [x["nom"].lower() for x in items]

    if "paracetamol" in noms and "methanol" in noms:
        interactions.append("⚠️ Risque hépatotoxique grave")

    if "aspirine" in noms and "ibuprofen" in noms:
        interactions.append("⚠️ Risque digestif élevé")

    if not interactions:
        interactions.append("✅ Aucune interaction connue")

    return interactions