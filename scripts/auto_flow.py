"""
Automated 100% Direct Login & Auto-Publish Orchestrator.
Uses provided MakerWorld credentials, solves 2FA verification via Telegram / chat,
captures session, auto-detects real user ID, and immediately publishes a 3D model to MakerWorld!
"""

import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
venv_python = BASE_DIR / "venv" / "bin" / "python3"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

sys.path.insert(0, str(BASE_DIR))

from config import get_config
from core.orchestrator import AutopilotOrchestrator
from uploader.session_manager import SessionManager


def run_auto_flow():
    print("\n=======================================================")
    print("  🚀 INICIANDO PUBLICACIÓN 100% AUTOMATIZADA")
    print("=======================================================")

    session_mgr = SessionManager()
    if not session_mgr.has_saved_session():
        print("🔑 Iniciando sesión automáticamente con las credenciales...")
        ok = session_mgr.direct_login(headless=False)
        if not ok:
            print("❌ No se pudo completar el inicio de sesión.")
            return

    print("\n=======================================================")
    print("  📦 GENERANDO Y PUBLICANDO MODELO EN MAKERWORLD...")
    print("=======================================================")
    orchestrator = AutopilotOrchestrator()
    res = orchestrator.run_cycle(auto_publish=True)
    print("\n🎉 ¡PROCESO COMPLETADO AL 100%!")
    print(f"Modelo publicado: {res.get('title')}")
    print(f"URL: {res.get('url')}")
    print("Revisa tu Telegram para ver la notificación y estadísticas.")


if __name__ == "__main__":
    run_auto_flow()
