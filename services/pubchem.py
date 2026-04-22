import requests

def search_pubchem(name):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/MolecularFormula,MolecularWeight/JSON"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()
        props = data["PropertyTable"]["Properties"][0]

        return {
            "source": "PubChem",
            "formula": props.get("MolecularFormula"),
            "poids_moleculaire": props.get("MolecularWeight")
        }
    except:
        return None