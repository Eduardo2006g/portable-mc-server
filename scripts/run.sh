#!/bin/bash


cd "$(dirname "$0")/.."

echo "=== Portable Minecraft Server Manager (Linux) ==="
echo "[DEBUG] Working Directory: $(pwd)"


if [ ! -d ".venv" ]; then
    echo "[INFO] Virtual environment not found. Creating it in the root directory..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Failed to create venv."
        exit 1
    fi
fi


echo "[INFO] Activating the virtual enviroment..."
source .venv/bin/activate


if [ ! -f "scripts/.venv/.deps_installed" ]; then
    if [ -f "requirements.txt" ]; then
        echo "[INFO] Installing dependencies from the root directory, wait until its finished..."
        python3 -m pip install --upgrade pip
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "ok" > "scripts/.venv/.deps_installed"
        else
            echo "[ERRO] Failed to install dependencies."
            exit 1
        fi
    else
        echo "[ERRO] requirements.txt not found in the root directory!"
        exit 1
    fi
fi


if ! docker info > /dev/null 2>&1; then
    echo "[ERRO] Docker is not running! Make sure the Docker daemon is active."
    exit 1
fi


case "$1" in
    start)
        echo "[INFO] Starting Containers and Server..."
        docker compose up -d
        export PYTHONPATH=$(pwd)
        python3 scripts/start.py
        ;;
    stop)
        echo "[INFO] Stopping Server and Containers..."
        export PYTHONPATH=$(pwd)
        python3 scripts/stop.py
        docker compose down
        ;;
    docker)
        echo "[INFO] Starting the Containers only..."
        docker compose up -d
        export PYTHONPATH=$(pwd)
        ;;
    interface)
        echo "[INFO] Initializing Streamlit Interface..."
        python3 -m streamlit run app.py
        export PYTHONPATH=$(pwd)
        ;;
esac