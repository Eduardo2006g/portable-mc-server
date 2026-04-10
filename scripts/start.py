import sys
from server import start_server, is_server_running
from config import MEU_NOME, TAILSCALE_IPS, MINECRAFT_PORT

if __name__ == "__main__":
    if is_server_running():
        print("⚠️ Server is already running. Use stop.py to stop it before starting again.")
        sys.exit(0)

    print("=" * 50)
    print("🎮 MINECRAFT SERVER — STARTING")
    print("=" * 50)

    ok = start_server()

    if ok:
        meu_ip = TAILSCALE_IPS.get(MEU_NOME, "?")
        print("\n" + "=" * 50)
        print(f"✅ READY!")
        print(f"   Connect at: {meu_ip}:{MINECRAFT_PORT}")
        print("=" * 50)
        print("When done, run: python stop.py")