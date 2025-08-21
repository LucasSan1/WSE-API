from fastapi import FastAPI, Query
from src.processors.populationProcessor import searchFilter, load_data, normalize_text
from src.scrapers.ibgeScraper import download_data, needs_update

# Intervalo: 1 mês ≈ 30 dias
UPDATE_INTERVAL = 30 * 24 * 60 * 60  # 2.592.000 segundos

app = FastAPI(
    title="WSE API",
    description="API para consulta de população por município ou UF",
    version="1.0.0",
)

def ensure_data():
    # Baixa os dados se estiverem desatualizados
    if needs_update(UPDATE_INTERVAL):
        download_data()

# ---------- Endpoints Populacao----------

@app.get("/populacao")
def get_populacao(term: str = Query(..., description="Município ou UF para busca")):
    ensure_data()
    results = searchFilter(term)
    if not results:
        return {"mensagem": f"Nenhum resultado encontrado para '{term}'"}
    return {"resultados": results}

@app.get("/populacao/total-uf")
def total_uf():
    ensure_data()
    data = load_data()
    total = {}
    for item in data:
        uf = item.get("D1N")
        pop = int(item.get("V", 0))
        total[uf] = total.get(uf, 0) + pop
    return total

@app.get("/populacao/municipio-maior")
def municipio_maior(uf: str = None):
    ensure_data()
    data = load_data()
    max_pop = -1
    result = {}
    for item in data:
        if uf and normalize_text(item.get("D1N", "")) != normalize_text(uf):
            continue
        pop = int(item.get("V", 0))
        if pop > max_pop:
            max_pop = pop
            result = {"municipio": item.get("D1N"), "populacao": pop}
    return result

@app.get("/populacao/municipio-menor")
def municipio_menor(uf: str = None):
    ensure_data()
    data = load_data()
    min_pop = float("inf")
    result = {}
    for item in data:
        if uf and normalize_text(item.get("D1N", "")) != normalize_text(uf):
            continue
        pop = int(item.get("V", 0))
        if pop < min_pop:
            min_pop = pop
            result = {"municipio": item.get("D1N"), "populacao": pop}
    return result
