@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0.."

echo === Portable Minecraft Server Manager ===
echo [DEBUG] Pasta atual: %CD%

REM 
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Creating it in the root directory...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment successfully created
)

REM 
echo [INFO] Activating the virtual enviroment...
call .venv\Scripts\activate.bat

REM 
if not exist ".venv\.deps_installed" (
    if exist "requirements.txt" (
        echo [INFO] Installing dependencies from the root directory, wait until its finished... 
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        if !errorlevel! EQU 0 (
            echo ok > ".venv\.deps_installed"
        )
    )
)

REM 
docker info >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [ERROR] Docker is not running! Make sure the Docker daemon is active.
    pause
    exit /b 1
)

REM 
if "%1"=="start" goto :START_SERVER
if "%1"=="stop" goto :STOP_SERVER
if "%1"=="docker" goto :DOCKER_ONLY
if "%1"=="interface" goto :INTERFACE

:START_SERVER
echo [INFO] Starting Containers and Server...
docker compose up -d
set PYTHONPATH=%CD%
python scripts\start.py
goto :EOF

:STOP_SERVER
echo [INFO] Stopping Server and Containers...
set PYTHONPATH=%CD%
python scripts\stop.py
docker compose down
goto :EOF

:DOCKER_ONLY
echo [INFO] Starting the Containers only...
docker compose up -d
goto :EOF

:INTERFACE
echo [INFO] Initializing Streamlit Interface...
python -m streamlit run app.py
goto :EOF