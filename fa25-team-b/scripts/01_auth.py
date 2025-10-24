import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.google_drive import get_drive_service

if __name__ == "__main__":
    get_drive_service()
    print("✅ Auth complete. Token saved to secrets/token.json")