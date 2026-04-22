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

    item["toxicologie"] = {
        "classe": danger,
        "voie_exposition": "orale",
        "effets": "dose dépendante"
    }

    return item