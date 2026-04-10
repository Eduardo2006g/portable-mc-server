import sys
from server import stop_server

if __name__ == "__main__":
    print("=" * 50)
    print("🎮 MINECRAFT SERVER — CLOSING DOWN")
    print("=" * 50)

    confirm = input("\nAre you sure you want to stop? (s/n): ").strip().lower()
    if confirm != "s":
        print("Canceled.")
        sys.exit(0)

    stop_server()

    print("\n" + "=" * 50)
    print("✅ All saved. World available for the next session!")
    print("=" * 50)