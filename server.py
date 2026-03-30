import os
import io
import shutil
import zipfile
import subprocess
import requests
from pathlib import Path
from config import *
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

BASE_DIR = Path(__file__).parent


# google drive

def get_drive_service():

    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    token_path = BASE_DIR / "token.json"
    creds_path = BASE_DIR / "credentials.json"

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                raise FileNotFoundError("credentials.json não encontrado. Siga o Passo 2 do guia.")
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def download_world(log=print):
    log("📥 Procurando mundo no Google Drive...")
    service = get_drive_service()

    results = service.files().list(
        q=f"name='{WORLD_FILENAME}' and '{DRIVE_FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name, modifiedTime)"
    ).execute()
    files = results.get("files", [])

    if not files:
        log("ℹ️ Nenhum mundo no Drive. Iniciando do zero.")
        return False

    file = files[0]
    log(f"✅ Mundo encontrado (modificado em {file['modifiedTime']})")
    log("⬇️ Baixando...")

    zip_path = BASE_DIR / WORLD_FILENAME
    request = service.files().get_media(fileId=file["id"])
    
    with io.FileIO(str(zip_path), "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    log("📦 Extraindo mundo...")
    world_dir = BASE_DIR / "world-data"
    if world_dir.exists():
        shutil.rmtree(world_dir)
    world_dir.mkdir()

    with zipfile.ZipFile(str(zip_path), "r") as zf:
        zf.extractall(str(world_dir))

    zip_path.unlink()
    log("✅ Mundo restaurado!")
    return True

def upload_world(log=print):
    world_dir = BASE_DIR / "world-data"
    if not world_dir.exists():
        log("⚠️ Pasta world-data não encontrada.")
        return

    log("📦 Comprimindo mundo...")
    zip_path = BASE_DIR / WORLD_FILENAME

    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for file in world_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(world_dir))

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    log(f"✅ Comprimido: {size_mb:.1f} MB")

    log("⬆️ Enviando pro Google Drive...")
    service = get_drive_service()

    results = service.files().list(
        q=f"name='{WORLD_FILENAME}' and '{DRIVE_FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute()
    files = results.get("files", [])

    with open(str(zip_path), "rb") as f:
        media = MediaIoBaseUpload(
            f,
            mimetype="application/zip",
            resumable=True,
            chunksize=10 * 1024 * 1024  # 10MB por chunk
        )

        if files:
            request = service.files().update(
                fileId=files[0]["id"],
                media_body=media
            )
        else:
            request = service.files().create(
                body={"name": WORLD_FILENAME, "parents": [DRIVE_FOLDER_ID]},
                media_body=media
            )

        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    log(f"⬆️ Upload: {progress}%")
            except Exception as e:
                log(f"⚠️ Erro no upload, tentando novamente: {e}")

    try:
        zip_path.unlink()
        log("✅ Mundo salvo no Google Drive!")

    except Exception as e:
        log(f"⚠️ Não foi possível apagar o zip local, mas o upload foi feito: {e}")

# discord

def notify_discord(message):
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=5)
    except:
        pass


# docker

def is_server_running():
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=minecraft", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return "minecraft" in result.stdout


def start_docker(log=print):
    compose_path = BASE_DIR / "docker-compose.yml"
    env = os.environ.copy()
    env["MINECRAFT_VERSION"] = MINECRAFT_VERSION
    env["MINECRAFT_TYPE"] = MINECRAFT_TYPE
    env["MINECRAFT_MEMORY"] = MINECRAFT_MEMORY
    #env["WHITELIST"] = ",".join(WHITELIST_PLAYERS)

    log("🚀 Subindo servidor Minecraft...")
    result = subprocess.run(
        ["docker", "compose", "-f", str(compose_path), "up", "-d"],
        env=env, capture_output=True, text=True
    )

    if result.returncode != 0:
        log(f"❌ Erro ao subir Docker: {result.stderr}")
        return False

    log("✅ Servidor no ar!")
    return True


def stop_docker(log=print):
    compose_path = BASE_DIR / "docker-compose.yml"
    log("🛑 Parando servidor...")
    subprocess.run(["docker", "compose", "-f", str(compose_path), "down"])
    log("✅ Servidor parado.")


# fluxos principais

def start_server(log=print):
    download_world(log)

    if not start_docker(log):
        return False

    meu_ip = TAILSCALE_IPS.get(MEU_NOME, "IP não configurado")
    notify_discord(
        f"🟢 **Servidor no ar!**\n"
        f"Hosteado por: **{MEU_NOME}**\n"
        f"Conecte em: `{meu_ip}:{MINECRAFT_PORT}`"
    )
    return True


def stop_server(log=print):
    stop_docker(log)
    upload_world(log)
    notify_discord(f"🔴 **Servidor encerrado** por **{MEU_NOME}**. Mundo salvo no Drive!")