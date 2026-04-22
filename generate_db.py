import json

data = []

base = [
("neem","plante",5000),
("paracetamol","medicament",338),
("methanol","chimique",5628),
("ibuprofen","medicament",636),
("aspirine","medicament",200),
("cafeine","chimique",192),
("nicotine","toxique",50),
("quinine","medicament",660),
("arsenic","toxique",15),
("chloroquine","medicament",620),
]

# duplication intelligente
for i in range(1,501):
    name, t, dl = base[i % len(base)]
    data.append({
        "id": i,
        "nom": f"{name}_{i}",
        "dl50": dl,
        "type": t
    })

with open("data/database.json","w",encoding="utf-8") as f:
    json.dump(data,f,indent=2)

print("✅ 500 substances créées")