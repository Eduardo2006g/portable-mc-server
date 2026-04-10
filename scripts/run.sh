#!/bin/bash

# entra na raiz do projeto
cd "$(dirname "$0")/.."

echo "=== Portable Minecraft Server Manager (Linux) ==="
echo "[DEBUG] Working Directory: $(pwd)"

# verifica se a venv existe, se não, cria uma
if [ ! -d ".venv" ]; then
    echo "[INFO] Ambiente virtual nao encontrado. Criando na raiz..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar venv."
        exit 1
    fi
fi

# ativa venv
echo "[INFO] Ativando ambiente virtual..."
source .venv/bin/activate

# instala depedencias
if [ ! -f "scripts/.venv/.deps_installed" ]; then
    if [ -f "requirements.txt" ]; then
        echo "[INFO] Instalando dependencias a partir da raiz..."
        python3 -m pip install --upgrade pip
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "ok" > "scripts/.venv/.deps_installed"
        else
            echo "[ERRO] Falha ao instalar dependencias."
            exit 1
        fi
    else
        echo "[ERRO] requirements.txt nao encontrado na raiz!"
        exit 1
    fi
fi

# verifica se o docker tá rodando
if ! docker info > /dev/null 2>&1; then
    echo "[ERRO] Docker nao esta rodando! Certifique-se de que o daemon do Docker esta ativo."
    exit 1
fi

# roteamento dos comandos
case "$1" in
    start)
        echo "[INFO] Subindo Containers e Servidor..."
        docker compose up -d
        export PYTHONPATH=$(pwd)
        python3 scripts/start.py
        ;;
    stop)
        echo "[INFO] Parando Servidor e Containers..."
        export PYTHONPATH=$(pwd)
        python3 scripts/stop.py
        docker compose down
        ;;
    docker)
        echo "[INFO] Subindo apenas Containers..."
        docker compose up -d
        ;;
    *)
        echo "[INFO] Iniciando Interface Streamlit..."
        # roda streamlit
        python3 -m streamlit run app.py
        ;;
esac
