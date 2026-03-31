
# 🌍 Portable Minecraft Server 

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Tailscale](https://img.shields.io/badge/Tailscale-Mesh_Network-black.svg)
![Radmin VPN](https://img.shields.io/badge/RadminVPN-LAN_Emulation-blue.svg)

A fully decentralized and portable Minecraft server. Any group member can host the server on their own computer, with the world automatically syncing via Google Drive and network routing handled through a virtual network (Tailscale or Radmin VPN).

Goodbye paid hosting and router port forwarding!

---

## 🏗️ Architecture

This project breaks the traditional game server model by separating responsibilities:

- **Compute (Local):**  
  The server runs inside a Docker container (`itzg/minecraft-server`), ensuring a consistent environment across all operating systems.

- **Network (Virtual LAN / Mesh VPN):**  
  You can choose between:
  - **Tailscale:** Secure mesh VPN with fixed `100.x.x.x` IPs
  - **Radmin VPN:** LAN emulation with `26.x.x.x` IPs

- **Storage (Cloud):**  
  The world (`world-data`) is compressed and uploaded to a shared Google Drive folder when the server stops, and automatically downloaded when it starts.

---

## 🚀 Getting Started

### Pre-requisites

All players must install:

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine on Linux)
2. One of the following:
   - [Tailscale](https://tailscale.com/) (logged into the same network)
   - Radmin VPN (connected to the same virtual LAN)
3. [Python 3.8+](https://www.python.org/downloads/)

---

### Initial Setup (One-time only)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ilhe8l/portable-mc-server.git
   cd portable-mc-server
   ```

2. **Google Drive Authentication:**

   * Create a project in Google Cloud Console
   * Enable Google Drive API
   * Create OAuth 2.0 credentials (Desktop App)
   * Download the file, rename it to `credentials.json`, and place it in the root folder

3. **Configure variables:**
   Open `config.py` and set:

   * `DRIVE_FOLDER_ID`: Shared Google Drive folder ID
   * `DISCORD_WEBHOOK_URL`: (Optional) Discord webhook
   * `TAILSCALE_IPS`: Map player names to their IPs (Tailscale or Radmin)
   * `MEU_NOME`: Your identifier (must match the dictionary key)

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎁 Alternative Quick Start (Windows)

### ⚠️ Complete setup up to step 3 before using this ⚠️

The project includes a **`run.bat`** script (Windows only) that automates the remaining setup.

### Run via CMD / PowerShell

## 🟢 Starting the Server
```bash
.\run.bat start
```

This will:

* Activate (or create) the virtual environment
* Install dependencies (if needed)
* Start Docker containers
* Launch the Minecraft server

### Example output:

```bash
=== Portable Minecraft Server Manager ===
[INFO] Activating virtual environment...
[INFO] Starting containers and server...
[+] Running 2/2
 ✔ Network portable-mc-server_default  Created
 ✔ Container minecraft               Started

==================================================
🎮 MINECRAFT SERVER — STARTING
==================================================
📥 Checking world on Google Drive...
✅ World found (last modified: 2026-03-31)
⬇️ Downloading...
📦 Extracting world...
✅ World restored successfully!
🚀 Starting Minecraft server...
✅ Server is online!

==================================================
✅ READY!
Connect to: 26.xxx.xxx.xxx:25565
==================================================
```

## 🛑 Stopping the Server


```bash
.\run.bat stop
```
This will:

* Deactivate (or create) the virtual environment
* Safely stop the Minecraft server
* Shut down and remove Docker containers
* Compress the updated world data
* Upload the latest version to Google Drive

### Example output:
```bash
Stopping everything...
==================================================
🎮 MINECRAFT SERVER — SHUTTING DOWN
==================================================

Are you sure you want to stop? (y/n): y
🛑 Stopping server...
[+] Running 2/2
 ✔ Container minecraft                 Removed                                                                     
 ✔ Network portable-mc-server_default  Removed                                                                     
✅ Server stopped successfully.
📦 Compressing world...
✅ Compressed: x MB
⬆️ Uploading to Google Drive...
⬆️ Upload: ...%

✅ World successfully saved to Google Drive!

==================================================
✅ ALL DONE! World is ready for the next session.
==================================================
```

---

## 🎮 How to Use

The project includes a user-friendly interface built with Streamlit.

### Start the GUI

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

### Features

* **Start Server:**

  * Downloads the latest world from Google Drive
  * Extracts it
  * Starts Docker container
  * Sends Discord notification

* **Stop Server:**

  * Stops container safely
  * Compresses updated world
  * Uploads to Google Drive

---

## 🤝 How to Connect In-game

1. Open Minecraft (version defined in `docker-compose.yml`)
2. Go to **Multiplayer > Add Server**
3. Use the appropriate IP:

### Tailscale:

```
100.x.x.x:25565
```

### Radmin VPN:

```
26.x.x.x:25565
```

4. Connect to the host's IP when the server is running

---

## 🔒 Security and Usage Rules

* **Always stop the server properly:**
  Never close the terminal or shut down your PC while the server is running.
  Always use the Stop button or `stop.py`.

* **Avoid conflicts:**
  Only one person should run the server at a time.
  Running multiple instances can overwrite the world stored in Google Drive.

---

## 💡 Notes

* Tailscale is more secure and stable for internet-based play
* Radmin VPN is simpler and ideal for LAN-like environments
* Both options are fully supported by this project
