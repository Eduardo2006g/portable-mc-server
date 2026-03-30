import os
from dotenv import load_dotenv
import json

load_dotenv()

# Google Drive
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
WORLD_FILENAME = os.getenv("WORLD_FILENAME", "minecraft-world.zip")

# Discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Tailscale IPs (formato: JSON string no .env)
TAILSCALE_IPS = json.loads(os.getenv("TAILSCALE_IPS", "{}"))

# Nome (usado na mensagem do discord)
MEU_NOME = os.getenv("MEU_NOME", "Guilherme")

# Servidor Minecraft
MINECRAFT_VERSION = os.getenv("MINECRAFT_VERSION", "1.21.4")
MINECRAFT_TYPE = os.getenv("MINECRAFT_TYPE", "PAPER")
MINECRAFT_MEMORY = os.getenv("MINECRAFT_MEMORY", "2G")

# Whitelist (lista separada por vírgula no .env)
WHITELIST_PLAYERS = os.getenv("WHITELIST_PLAYERS", "").split(",")

# Porta
MINECRAFT_PORT = int(os.getenv("MINECRAFT_PORT", 25565))