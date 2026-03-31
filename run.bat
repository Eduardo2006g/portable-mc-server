@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo === Portable Minecraft Server Manager ===

REM --- 1. Verificacao/Criacao da VENV ---
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtual nao encontrado. Criando agora...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar venv.
        pause
        exit /b 1
    )
    echo [OK] Venv criada com sucesso.
)

REM --- 2. Ativacao da VENV ---
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM --- 3. Instalacao de Dependencias ---
if not exist ".venv\.deps_installed" (
    if exist "requirements.txt" (
        echo [INFO] Instalando dependencias...
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        if %errorlevel% EQU 0 (
            echo Gravando trava de instalacao...
            echo ok > ".venv\.deps_installed"
        ) else (
            echo [ERRO] Falha ao instalar dependencias.
            pause
            exit /b 1
        )
    )
)

REM --- 4. Verificacao do Docker ---
docker info >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [ERRO] Docker nao esta rodando! Inicie o Docker Desktop.
    pause
    exit /b 1
)

REM --- 5. Roteamento de Comandos ---
if "%1"=="start" goto :START_SERVER
if "%1"=="stop" goto :STOP_SERVER
if "%1"=="docker" goto :DOCKER_ONLY

:INTERFACE
echo [INFO] Iniciando Interface Streamlit...
python -m streamlit run app.py
goto :EOF

:START_SERVER
echo [INFO] Subindo Containers e Servidor...
docker compose up -d
python start.py
goto :EOF

:STOP_SERVER
echo [INFO] Parando Servidor e Containers...
python stop.py
docker compose down
goto :EOF

:DOCKER_ONLY
echo [INFO] Subindo apenas Containers...
docker compose up -d
goto :EOF