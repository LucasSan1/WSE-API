import os
import subprocess
import sys

# Caminho do .venv
VENV_PATH = os.path.join(os.path.dirname(__file__), ".venv")

# Caminho para o Python dentro do .venv
python_executable = os.path.join(VENV_PATH, "bin", "python")

# Comando para rodar o uvicorn
cmd = [
    python_executable,
    "-m",
    "uvicorn",
    "src.api.main:app",
    "--host", "127.0.0.1",
    "--port", "8000",
    "--reload"
]

# Rodar o comando
subprocess.run(cmd, cwd=os.path.dirname(__file__))
