📦 portable-mc-server
 ┣ 📂 .venv                # Virtual environment (automatically created in root)
 ┣ 📂 auth                 # Google Drive credentials (Protected by .gitignore)
 ┃ ┣ 📜 credentials.json
 ┃ ┗ 📜 token.json
 ┣ 📂 docs                 # Project documentation
 ┃ ┣ 📜 Mods.md            # Mod installation guide
 ┃ ┗ 📜 tree.md            # Project structure documentation
 ┣ 📂 scripts              # Automation and support scripts
 ┃ ┣ 📜 run.bat            # Main execution script (Windows)
 ┃ ┣ 📜 run.sh             # Main execution script (Linux)
 ┃ ┣ 📜 start.py           # Python startup logic
 ┃ ┗ 📜 stop.py            # Python shutdown logic
 ┣ 📜 .env                 # Local environment variables (Not versioned)
 ┣ 📜 .env.example         # Template for new users
 ┣ 📜 .gitattributes       # Git path and attribute configurations
 ┣ 📜 .gitignore           # Git exclusion rules
 ┣ 📜 app.py               # Streamlit interface (Main Entrypoint)
 ┣ 📜 config.py            # Configuration variables and Path management
 ┣ 📜 docker-compose.yml   # Minecraft container orchestration
 ┣ 📜 README.md            # Main user manual
 ┣ 📜 requirements.txt     # Python dependencies
 ┗ 📜 server.py            # Core server management functions