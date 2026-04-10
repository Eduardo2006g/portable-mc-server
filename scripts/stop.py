import sys
from server import stop_server

if __name__ == "__main__":
    print("=" * 50)
    print("🎮 SERVIDOR MINECRAFT — ENCERRANDO")
    print("=" * 50)

    confirm = input("\nTem certeza que quer parar? (s/n): ").strip().lower()
    if confirm != "s":
        print("Cancelado.")
        sys.exit(0)

    stop_server()

    print("\n" + "=" * 50)
    print("✅ Tudo salvo. Mundo disponível pra próxima sessão!")
    print("=" * 50)