"""
Session and Authentication Manager for MakerWorld.
Maintains persistent browser profiles and cookies so logins survive across autonomous runs.
Equipped with Cloudflare Turnstile anti-bot bypass & Real Chrome launch support.
"""

import os
import re
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional


class SessionManager:
    def __init__(self, profile_dir: Optional[Path] = None):
        if profile_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
            profile_dir = base_dir / "data" / "browser_profile"
        
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.profile_dir / "storage_state.json"

    def has_saved_session(self) -> bool:
        """Checks if a saved browser session state exists."""
        return self.state_file.exists() and self.state_file.stat().st_size > 100

    def _update_user_id_in_config(self, user_id: str) -> None:
        """Automatically updates makerworld.user_id in config.yaml with the real user ID."""
        config_file = Path(__file__).resolve().parent.parent / "config.yaml"
        if not config_file.exists():
            return
        try:
            content = config_file.read_text(encoding="utf-8")
            content = re.sub(
                r'user_id:\s*["\'].*?["\']',
                f'user_id: "{user_id}"',
                content
            )
            config_file.write_text(content, encoding="utf-8")
            print(f"⚙️ Configuración actualizada: makerworld.user_id = \"{user_id}\"")
        except Exception as e:
            print(f"[SessionManager] Warning updating config.yaml: {e}")

    def launch_real_chrome_login(self) -> bool:
        """
        Launches the official Google Chrome app on macOS with remote debugging.
        This completely bypasses Cloudflare Turnstile and Google SSO blocks because
        it is 100% genuine Google Chrome (not an automated Playwright instance).
        """
        chrome_bin = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if not chrome_bin.exists():
            return False

        port = 9222
        print("\n=======================================================")
        print("  🌐 INICIANDO GOOGLE CHROME OFICIAL (SIN BLOQUEOS)")
        print("=======================================================")
        print("Se ha abierto Google Chrome en tu pantalla.")
        print("1. En la ventana de Chrome que se ha abierto, pulsa 'Iniciar sesión'.")
        print("2. Entra con tu cuenta de Google o de Bambu Lab.")
        print("3. IMPORTANTE: NO pulses Enter en esta terminal hasta que veas tu foto de perfil en MakerWorld.\n")

        # Launch real Chrome in isolated profile with remote debugging
        cmd = [
            str(chrome_bin),
            f"--remote-debugging-port={port}",
            f"--user-data-dir={self.profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "https://makerworld.com/es"
        ]

        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)

        while True:
            try:
                input(">>> Pulsa [ENTER] ÚNICAMENTE después de haber completado el login en la ventana de Chrome: ")
            except EOFError:
                pass

            # Connect via Playwright to verify that the user is ACTUALLY logged in
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    try:
                        browser = p.chromium.connect_over_cdp(f"http://localhost:{port}")
                        contexts = browser.contexts
                        if not contexts:
                            print("⚠️ No se detecta ventana abierta de Chrome. Vuelve a intentarlo.")
                            continue

                        page = contexts[0].pages[0] if contexts[0].pages else contexts[0].new_page()
                        page.goto("https://makerworld.com/es", wait_until="domcontentloaded", timeout=20000)
                        time.sleep(3)

                        # Check if login button is still visible
                        has_login_btn = page.locator("button:has-text('Iniciar sesión'), a:has-text('Iniciar sesión'), button:has-text('Sign in')").count() > 0
                        if has_login_btn:
                            print("\n❌ AÚN NO HAS INICIADO SESIÓN:")
                            print("Todavía aparece el botón 'Iniciar sesión' en la ventana de Chrome.")
                            print("Por favor, pulsa 'Iniciar sesión' en Chrome, identifícate y cuando ya estés dentro, vuelve aquí y pulsa Enter.")
                            browser.close()
                            continue

                        # Extract real user ID from profile links
                        user_id = None
                        links = page.locator("a[href*='/u/']").all()
                        for l in links:
                            href = l.get_attribute("href") or ""
                            parts = [pt for pt in href.split("/") if pt]
                            if "u" in parts:
                                idx = parts.index("u")
                                if idx + 1 < len(parts):
                                    candidate = parts[idx + 1].split("?")[0]
                                    if candidate:
                                        user_id = candidate
                                        break

                        # Capture cookies & storage state
                        contexts[0].storage_state(path=str(self.state_file))
                        print(f"\n✅ ¡Sesión VERIFICADA y guardada con éxito en {self.state_file}!")
                        if user_id:
                            print(f"👤 Tu ID de usuario real de MakerWorld es: {user_id}")
                            self._update_user_id_in_config(user_id)
                        browser.close()
                        break
                    except Exception as e:
                        print(f"[SessionManager] Error verificando sesión vía CDP: {e}")
                        break
            except ImportError:
                break

        # Terminate the interactive Chrome process
        try:
            proc.terminate()
        except Exception:
            pass

        return True

    def launch_interactive_login(self) -> bool:
        """Launches interactive login via real Google Chrome."""
        return self.launch_real_chrome_login()
