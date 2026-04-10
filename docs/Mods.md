# 🤓 How to add mods to your service

To ensure your local Minecraft client and the remote server are perfectly synchronized, follow these steps to manage and update the mod list.

### 📁 Mod Management Strategy
For a NeoForge environment, mods are categorized into two types: **Synchronized Mods** (must be on both) and **Client-Side Mods** (your PC only).

| Mod Type | Location | Purpose | Examples |
| :--- | :--- | :--- | :--- |
| **Content Mods** | 💻 Client & ☁️ Server | New items, blocks, and dimensions. | *The Aether II, Waystones, Sophisticated Backpacks* |
| **Optimization** | 💻 Client Only | Performance and visual tweaks. | *Sodium, Iris, Just Zoom* |
| **UI / HUD** | 💻 Client Only | Map and interface information. | *Xaero’s Minimap, Jade, JEI* |

### 🚀 Step-by-Step: Adding New Mods

1.  **Download the `.jar`:** Ensure you are downloading the **NeoForge** version for Minecraft **1.21.8** or the required by your mod.
    ##### Example of change for this especific part of your `.env`:
```
# Minecraft
MINECRAFT_VERSION=1.21.8
MINECRAFT_TYPE=NEOFORGE
MINECRAFT_MEMORY=4G
```
2.  **Server-Side Upload:**
    * Navigate to your server's root directory.
    * Upload the file to the `world-data/mods` folder.
    * *Note:* If you are using the **Portable Minecraft Server** (Docker/Python), ensure the world sync or volume mapping is active.
3.  **Client-Side Install:**
    * Copy the same `.jar` file to your local `%appdata%\.minecraft\versions\...\mods` folder.
4.  **Configuration Sync:**
    * If a mod generates a specific config file (e.g., `sophisticatedbackpacks-common.toml`), it is highly recommended to copy the server's `config/` file to your client to avoid "Registry Mismatch" errors.

### ⚠️ Common Pitfalls
* **Version Mismatch:** Even a minor NeoForge sub-version difference (e.g., `.51` vs `.53`) can sometimes cause connection issues. Always aim for parity.
* **Missing Dependencies:** Check if the new mod requires a "Core" or "API" mod (like *Sophisticated Core* or *Balm*).
* **Channel Errors:** If you see "Channel missing on server side," it means the server failed to load the mod. Check the server console logs for `modloading-worker` errors.

---