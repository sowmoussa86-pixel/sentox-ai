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
    "poids_moleculaire": props.get("MolecularWeight"),
}
if(data.scientifique){
 html+=`
 <div class="card">
   <b>Données scientifiques:</b><br>
   Formule: ${data.scientifique.formula}<br>
   Poids moléculaire: ${data.scientifique.poids_moleculaire}
 </div>`;
}
    except:
        return None