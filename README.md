# WSE-API

WSE API é uma aplicação Python construída com **FastAPI** para fornecer acesso a dados estruturados sobre municípios e outras informações via endpoints REST.  
O projeto é modular, com separação entre **scrapers**, **processadores** de dados e a **API**.

## Tecnologias Utilizadas

- Python 3.13
- FastAPI
- Requests
- Uvicorn

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/LucasSan1/WSE-API.git
cd WSE-API
```

2. Crie e ative o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

Se preferir instalar manualmente:
```bash
pip install fastapi uvicorn requests
```

## Como Rodar

Na raiz do projeto, execute:
```bash
python run.py
```

A API estará disponível em: http://127.0.0.1:8000  
