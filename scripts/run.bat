@echo off
setlocal EnableDelayedExpansion

:: 1. MUITO IMPORTANTE: Sobe para a raiz do projeto
:: %~dp0 é a pasta /scripts. O .. volta para portable-mc-server
cd /d "%~dp0.."

echo === Portable Minecraft Server Manager ===
echo [DEBUG] Pasta atual: %CD%

REM --- 1. Verificacao/Criacao da VENV na Raiz ---
:: Note que agora usamos ".venv" direto, pois o "cd .." ja nos colocou na raiz
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtual nao encontrado. Criando na raiz...
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
:: A trava de instalacao agora tambem fica na raiz
if not exist ".venv\.deps_installed" (
    if exist "requirements.txt" (
        echo [INFO] Instalando dependencias...
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        if !errorlevel! EQU 0 (
            echo ok > ".venv\.deps_installed"
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
:: Como estamos na raiz, o app.py é encontrado diretamente
python -m streamlit run app.py
goto :EOF

:START_SERVER
echo [INFO] Subindo Containers e Servidor...
docker compose up -d
:: Aqui está o truque: define a raiz (..) como pasta de módulos
set PYTHONPATH=%CD%
python scripts\start.py
goto :EOF

:STOP_SERVER
echo [INFO] Parando Servidor e Containers...
set PYTHONPATH=%CD%
python scripts\stop.py
docker compose down
goto :EOF

:DOCKER_ONLY
echo [INFO] Subindo apenas Containers...
docker compose up -d
goto :EOF