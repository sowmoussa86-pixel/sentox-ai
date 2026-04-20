import json

with open("data/database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

full = []
for i in range(10):
    for item in data:
        new_item = item.copy()
        new_item["id"] = len(full) + 1
        full.append(new_item)

with open("data/database_300.json", "w", encoding="utf-8") as f:
    json.dump(full, f, indent=2, ensure_ascii=False)

print("Base 300 générée")