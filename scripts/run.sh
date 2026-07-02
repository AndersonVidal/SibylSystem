#!/usr/bin/env bash
set -euo pipefail

# Resolve a raiz do projeto a partir da localização deste script,
# independente do diretório de onde é executado.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"

echo "Iniciando Sibyl..."
echo ""

# Verifica ambiente virtual
if [ ! -f "$PYTHON" ]; then
    echo "Erro: ambiente virtual não encontrado em $VENV_DIR"
    echo "Crie o ambiente e instale as dependências:"
    echo "  python3 -m venv venv"
    echo "  pip install -r requirements.txt"
    exit 1
fi

cd "$PROJECT_DIR"

echo "Aplicando migrations..."
"$PYTHON" manage.py migrate
echo ""

echo "Inicializando servidor..."
echo ""
echo "Sibyl disponível em:"
echo "http://127.0.0.1:8000"
echo ""

"$PYTHON" manage.py runserver
