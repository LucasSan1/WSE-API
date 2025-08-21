import requests
import json
import os
import time

FILE_JSON = "data/raw/populacao_municipios_last.json"
FILE_TIMESTAMP = "data/raw/last_update.json"
os.makedirs("data/raw", exist_ok=True)

SIDRA_URL = "https://apisidra.ibge.gov.br/values/t/6579/n6/all/v/9324/p/last?formato=json"

def download_data():
    #Baixa os dados da SIDRA e salva no JSON local
    try:
        response = requests.get(SIDRA_URL)
        response.raise_for_status()
        data = response.json()

        # Salva o JSON
        with open(FILE_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Atualiza timestamp
        with open(FILE_TIMESTAMP, "w", encoding="utf-8") as f:
            json.dump({"last_update": time.time()}, f)

        print(f"[OK] Dados salvos em {FILE_JSON}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Não foi possível baixar os dados: {e}")
        return False
    
# Verifica se já passou o intervalo desde o último download
def needs_update(interval_seconds: int) -> bool:
    if not os.path.exists(FILE_JSON) or not os.path.exists(FILE_TIMESTAMP):
        return True
    try:
        with open(FILE_TIMESTAMP, "r", encoding="utf-8") as f:
            ts = json.load(f).get("last_update", 0)
        return (time.time() - ts) > interval_seconds
    except Exception:
        return True 
