"""
One-Step Complete Publisher:
Logs in with credentials + OTP code, saves session permanently,
generates a 3D model, renders, and publishes to MakerWorld live!
"""

import os
import sys
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
venv_python = BASE_DIR / "venv" / "bin" / "python3"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

sys.path.insert(0, str(BASE_DIR))

from config import get_config
from core.orchestrator import AutopilotOrchestrator
from uploader.session_manager import SessionManager


def main():
    parser = argparse.ArgumentParser(description="Authenticate and Publish Live")
    parser.add_argument("--code", help="Verification OTP code from Bambu Lab email")
    args = parser.parse_args()

    cfg = get_config()
    session_mgr = SessionManager()

    if args.code:
        # Save code to otp_file so session_manager picks it up immediately
        session_mgr.otp_file.write_text(args.code.strip(), encoding="utf-8")
        print(f"✅ Código {args.code} preparado para autenticación.")

    print("\n=======================================================")
    print("  🚀 INICIANDO LOGIN Y PUBLICACIÓN DIRECTA")
    print("=======================================================")

    # Always ensure session is valid
    ok = session_mgr.direct_login(headless=False)
    if not ok:
        print("❌ Error al iniciar sesión. Comprueba el código o vuelve a intentarlo.")
        sys.exit(1)

    print("\n=======================================================")
    print("  📦 GENERANDO MODELO 3D Y PUBLICANDO EN MAKERWORLD")
    print("=======================================================")
    orchestrator = AutopilotOrchestrator()
    res = orchestrator.run_cycle(auto_publish=True)

    print("\n=======================================================")
    print("  🎉 ¡TODO COMPLETADO CON ÉXITO!")
    print("=======================================================")
    print(f"Modelo: {res.get('title')}")
    print(f"URL:    {res.get('url')}")
    print("Revisa tu Telegram para ver el reporte y estadísticas.")


if __name__ == "__main__":
    main()
