# 🌍 Portable Minecraft Server 

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Tailscale](https://img.shields.io/badge/Tailscale-Mesh_Network-black.svg)

A fully decentralized and portable Minecraft server. Any group member can host the server on their own computer, with the world automatically syncing via Google Drive and network routing managed via Tailscale. 

Goodbye paid hosting and port forwarding on the router!

## 🏗️ Architecture

The project breaks the traditional game server paradigm by splitting responsibilities:
* **Compute (Local):** The server runs inside a Docker container (using the `itzg/minecraft-server` image), ensuring the execution environment is identical regardless of the host's operating system.
* **Network (Mesh VPN):** Tailscale creates a virtual private network. The `100.x.x.x` IPs are fixed per machine, allowing direct connections between players from anywhere in the world.
* **Storage (Cloud):** The game state (`world-data`) is compressed and uploaded to a shared Google Drive folder upon shutdown, and automatically downloaded upon startup.

---

## 🚀 Getting Started

### Prerequisites
All players must have installed on their machines:
1.  [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine on Linux)
2.  [Tailscale](https://tailscale.com/) (logged into the group's network)
3.  [Python 3.8+](https://www.python.org/downloads/)

### Initial Setup (One-time only)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ilhe8l/portable-mc-server.git
   cd portable-mc-server
   ```

2. **Google Drive Authentication:**
   * Create a project in the Google Cloud Console, enable the Google Drive API, and create OAuth 2.0 credentials (Desktop App).
   * Download the generated file, rename it to `credentials.json`, and place it in the project root.

3. **Configure the Variables:**
   Open the `config.py` file and fill in your group's information:
   * `DRIVE_FOLDER_ID`: The ID of the shared Google Drive folder.
   * `DISCORD_WEBHOOK_URL`: (Optional) URL to send "Server Online" notifications on Discord.
   * `TAILSCALE_IPS`: Dictionary mapping each player's name to their fixed Tailscale IP.
   * `MEU_NOME`: Your identifier (must match the key in the dictionary above).

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 How to Use

The project features a user-friendly graphical interface built with Streamlit to make server management easy for any group member.

### Starting the GUI
In the terminal, run:
```bash
streamlit run app.py
```
Access `http://localhost:8501` in your browser.

* **Start the Server:** The script downloads the latest `.zip` from Drive, extracts it, initializes the Docker container, and notifies Discord of the IP hosting the session.
* **Stop the Server:** The script safely stops the container, compresses the updated map, and uploads the new version to Google Drive.

### CLI Alternative (Terminal)
If you prefer using the terminal directly without the GUI:
* To start: `python start.py`
* To stop and save: `python stop.py`

---

## 🤝 How to Connect In-game

1. Open Minecraft (version configured in `docker-compose.yml`).
2. Go to **Multiplayer > Add Server**.
3. Add the Tailscale IPs of all your friends (e.g., `100.x.x.x:25565`).
4. When someone starts the server, simply connect to that person's IP.

## 🔒 Security and Usage Rules
* **Wait for Shutdown:** Never force close the terminal or restart your computer while the server is running. Always use the "Stop" button or `stop.py` to ensure the map is saved to the cloud.
* **Avoid Conflicts:** Check Discord to see if someone has already started the server before starting yours. Two instances running simultaneously can overwrite each other's progress on Google Drive.
