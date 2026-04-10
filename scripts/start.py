import sys
from server import start_server, is_server_running
from config import MEU_NOME, TAILSCALE_IPS, MINECRAFT_PORT

if __name__ == "__main__":
    if is_server_running():
        print("⚠️ Servidor já está rodando. Use stop.py para parar antes de iniciar novamente.")
        sys.exit(0)

    print("=" * 50)
    print("🎮 SERVIDOR MINECRAFT — INICIANDO")
    print("=" * 50)

    ok = start_server()

    if ok:
        meu_ip = TAILSCALE_IPS.get(MEU_NOME, "?")
        print("\n" + "=" * 50)
        print(f"✅ PRONTO!")
        print(f"   Conecte em: {meu_ip}:{MINECRAFT_PORT}")
        print("=" * 50)
        print("Quando terminar, rode: python stop.py")