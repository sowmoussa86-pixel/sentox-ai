def suggest(name, data):
    suggestions = []
    for item in data:
        if name.lower()[:3] in item["nom"].lower():
            suggestions.append(item["nom"])
    return list(set(suggestions))[:5]