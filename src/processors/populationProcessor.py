import json
import os
import unicodedata

FILE_JSON = "data/raw/populacao_municipios_last.json"

# Dicionário para aceitar siglas de UF
SIGLAS_UF = {
    "ac": "Acre", "al": "Alagoas", "ap": "Amapá", "am": "Amazonas",
    "ba": "Bahia", "ce": "Ceará", "df": "Distrito Federal", "es": "Espírito Santo",
    "go": "Goiás", "ma": "Maranhão", "mt": "Mato Grosso", "ms": "Mato Grosso do Sul",
    "mg": "Minas Gerais", "pa": "Pará", "pb": "Paraíba", "pr": "Paraná",
    "pe": "Pernambuco", "pi": "Piauí", "rj": "Rio de Janeiro", "rn": "Rio Grande do Norte",
    "rs": "Rio Grande do Sul", "ro": "Rondônia", "rr": "Roraima", "sc": "Santa Catarina",
    "sp": "São Paulo", "se": "Sergipe", "to": "Tocantins"
}

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()

def load_data() -> list:
    # Carrega os dados do JSON, ignorando metadados.
    if not os.path.exists(FILE_JSON):
        raise FileNotFoundError(f"Arquivo {FILE_JSON} não encontrado!")
    
    with open(FILE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data[1:]  # Ignora o primeiro registro (metadados)

def searchFilter(term: str) -> list:
    term = normalize_text(term.strip())
    
    if term in SIGLAS_UF:
        term = normalize_text(SIGLAS_UF[term])
    
    results = []
    for item in load_data():
        municipio = normalize_text(item.get("D1N", ""))
        uf = normalize_text(item.get("D1N", ""))
        if term in municipio or term in uf:
            results.append({
                "unidade medida": item.get("MN"),
                "municipio": item.get("D1N"),
                "uf": item.get("D1N"),
                "codigo_municipio": item.get("D1C"),
                "ano": item.get("D3N"),
                "populacao": item.get("V")
            })
    return results

if __name__ == "__main__":
    term = input("Digite o município ou UF: ")
    results = searchFilter(term)

    if results:
        print(f"Resultados encontrados para '{term}':")
        for r in results[:10]:
            print(f"{r['municipio']} ({r['uf']}): {r['populacao']} habitantes")
        print(f"... {len(results)} resultados no total.")
    else:
        print(f"Nenhum resultado encontrado para '{term}'.")
