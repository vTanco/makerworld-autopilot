"""
Session and Authentication Manager for MakerWorld.
Maintains persistent browser profiles and cookies so logins survive across autonomous runs.
Equipped with direct programmatic login, Telegram 2FA OTP interception, and session persistence.
"""

import os
import re
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class SessionManager:
    def __init__(self, profile_dir: Optional[Path] = None):
        base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        if profile_dir is None:
            profile_dir = base_dir / "data" / "browser_profile"
        
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.profile_dir / "storage_state.json"
        self.otp_file = self.base_dir / "data" / "otp_code.txt"

    def has_saved_session(self) -> bool:
        """Checks if a saved browser session state exists and is not empty."""
        return self.state_file.exists() and self.state_file.stat().st_size > 100

    def _update_user_id_in_config(self, user_id: str) -> None:
        """Automatically updates makerworld.user_id in config.yaml with the real user ID."""
        config_file = self.base_dir / "config.yaml"
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

    def _send_telegram_alert(self, text: str) -> None:
        """Sends an urgent notification to the configured Telegram chat."""
        try:
            from config import get_config
            cfg = get_config()
            token = cfg.get("distribution.webhooks.telegram_bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = cfg.get("distribution.webhooks.telegram_chat_id") or os.getenv("TELEGRAM_CHAT_ID")
            if token and chat_id:
                import requests
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                    timeout=10
                )
        except Exception as e:
            print(f"[SessionManager] Warning sending Telegram message: {e}")

    def _wait_for_verification_code(self, timeout_seconds: int = 300) -> Optional[str]:
        """
        Listens for the 2FA / OTP verification code from Telegram or local otp_code.txt file.
        """
        from config import get_config
        cfg = get_config()
        token = cfg.get("distribution.webhooks.telegram_bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = str(cfg.get("distribution.webhooks.telegram_chat_id") or os.getenv("TELEGRAM_CHAT_ID") or "")

        last_update_id = 0
        if token:
            try:
                import requests
                r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset=-1", timeout=5)
                data = r.json()
                if data.get("ok") and data.get("result"):
                    last_update_id = data["result"][-1]["update_id"]
            except Exception:
                pass

        alert_msg = (
            "🔐 <b>MakerWorld / Bambu Lab - Código de Verificación</b>\n\n"
            "Bambu Lab ha enviado un código de seguridad a tu correo electrónico:\n"
            "📧 <code>vtancoagua@educacion.navarra.es</code>\n\n"
            "👉 <b>Responde directamente a este mensaje en Telegram con el código</b> (o escríbelo en el chat) para que el bot inicie sesión automáticamente."
        )
        self._send_telegram_alert(alert_msg)
        print("\n" + "="*60)
        print("  🔐 CÓDIGO DE VERIFICACIÓN SOLICITADO POR BAMBU LAB")
        print("="*60)
        print("Bambu Lab ha enviado un código a: vtancoagua@educacion.navarra.es")
        print("👉 Puedes responder directamente en Telegram al bot,")
        print("👉 o escribirlo en el chat del asistente,")
        print(f"👉 o guardarlo en: {self.otp_file}")
        print("="*60 + "\n")

        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            # 1. Check local file
            if self.otp_file.exists():
                try:
                    code = self.otp_file.read_text(encoding="utf-8").strip()
                    if code:
                        self.otp_file.unlink(missing_ok=True)
                        print(f"✅ Código recibido desde archivo: {code}")
                        return code
                except Exception:
                    pass

            # 2. Check Telegram updates
            if token:
                try:
                    import requests
                    r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}&timeout=3", timeout=6)
                    data = r.json()
                    if data.get("ok") and data.get("result"):
                        for upd in data["result"]:
                            last_update_id = max(last_update_id, upd["update_id"])
                            msg = upd.get("message", {})
                            msg_sender = str(msg.get("chat", {}).get("id", ""))
                            msg_text = msg.get("text", "").strip()
                            if chat_id and msg_sender != chat_id:
                                continue
                            # Extract 4-8 digit code
                            digits = re.findall(r"\b\d{4,8}\b", msg_text)
                            if digits:
                                found_code = digits[0]
                                print(f"✅ Código recibido desde Telegram: {found_code}")
                                self._send_telegram_alert(f"✅ Código <code>{found_code}</code> recibido. Validando inicio de sesión...")
                                return found_code
                except Exception:
                    pass

            time.sleep(2)

        print("❌ Tiempo de espera agotado para el código de verificación.")
        return None

    def direct_login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        headless: bool = False
    ) -> bool:
        """
        Executes 100% direct automated login using user credentials.
        Fills email, password, accepts terms, submits, and handles email OTP if challenged.
        Saves session cookies and updates makerworld.user_id.
        """
        from config import get_config
        cfg = get_config()

        email = email or cfg.get("makerworld.email") or os.getenv("MAKERWORLD_EMAIL") or "vtancoagua@educacion.navarra.es"
        password = password or cfg.get("makerworld.password") or os.getenv("MAKERWORLD_PASSWORD") or "Vt23011995."

        if not email or not password:
            print("[SessionManager] Error: Credenciales de MakerWorld no configuradas.")
            return False

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[SessionManager] Error: Playwright no instalado.")
            return False

        print("\n=======================================================")
        print("  🔑 INICIANDO SESIÓN AUTOMÁTICA EN MAKERWORLD")
        print("=======================================================")
        print(f"Cuenta: {email}")

        stealth_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-sandbox",
            "--no-first-run",
            "--no-default-browser-check"
        ]

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=headless,
                args=stealth_args,
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1400, "height": 900}
            )

            # Mask webdriver
            browser.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page = browser.new_page()
            login_url = "https://makerworld.com/es/sign-in/service?cb=https%3A%2F%2Fmakerworld.com%2Fmy%2Fmodels%2Fpublish"
            page.goto(login_url, wait_until="domcontentloaded", timeout=40000)
            time.sleep(3)

            # Accept cookies if banner visible
            try:
                accept_cookies = page.locator("button:has-text('Aceptar Todo'), button:has-text('Aceptar todo'), button:has-text('Accept All')").first
                if accept_cookies.is_visible(timeout=3000):
                    accept_cookies.click(force=True)
                    time.sleep(1)
            except Exception:
                pass

            # Check if already logged in (redirected to publish page)
            has_login_btn = page.locator("button:has-text('Iniciar sesión'), a:has-text('Iniciar sesión'), button:has-text('Sign in')").count() > 0
            is_sign_in_page = "sign-in" in page.url or "login" in page.url

            if not is_sign_in_page and not has_login_btn and "publish" in page.url:
                print("✅ Ya existe una sesión activa y válida en MakerWorld.")
                browser.storage_state(path=str(self.state_file))
                browser.close()
                return True

            # Fill Email
            email_input = page.locator("input[placeholder*='correo'], input[type='text'], input[type='email']").first
            if email_input.count() > 0:
                email_input.fill(email)
                time.sleep(0.5)

            # Fill Password
            pass_input = page.locator("input[type='password']").first
            if pass_input.count() > 0:
                pass_input.fill(password)
                time.sleep(0.5)

            # Check Terms of Service Checkbox
            checkbox = page.locator("input[type='checkbox']").first
            if checkbox.count() > 0:
                if not checkbox.is_checked():
                    checkbox.check(force=True)
                time.sleep(0.5)

            # Click Iniciar sesión
            submit_btn = page.locator("button:has-text('Iniciar sesión')").first
            if submit_btn.count() > 0:
                submit_btn.click()
                print("Formulario de login enviado, procesando respuesta...")
                time.sleep(3)

            # Wait for response: either redirect or verification code modal
            code_modal = page.locator("div:has-text('Código de Verificación'), input[placeholder*='verificac'], input[placeholder*='Código']").first
            is_modal = False
            for _ in range(8):
                time.sleep(1)
                try:
                    if code_modal.is_visible():
                        is_modal = True
                        break
                except Exception:
                    pass
                if "sign-in" not in page.url and "login" not in page.url and "makerworld.com" in page.url:
                    break

            if is_modal:
                print("⚠️ Bambu Lab requiere el código de verificación por correo.")
                otp_code = self._wait_for_verification_code(timeout_seconds=300)
                if otp_code:
                    code_field = page.locator("input[placeholder*='verificac'], input[placeholder*='Código'], input[type='text']").last
                    code_field.fill(otp_code)
                    time.sleep(1)
                    confirm_btn = page.locator("button:has-text('Confirmar'), button:has-text('Confirm')").first
                    if confirm_btn.count() > 0:
                        confirm_btn.click()
                        print("Botón Confirmar pulsado...")
                        time.sleep(5)
                else:
                    browser.close()
                    return False

            # Wait for redirect to makerworld
            logged_in = False
            user_id = None
            for _ in range(15):
                time.sleep(2)
                curr_url = page.url
                if "sign-in" not in curr_url and "login" not in curr_url and ("makerworld.com" in curr_url or "publish" in curr_url):
                    logged_in = True
                    break

            if logged_in:
                # Try to extract user ID from links or avatar
                time.sleep(2)
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

                browser.storage_state(path=str(self.state_file))
                print(f"\n✅ ¡Inicio de sesión COMPLETADO y guardado en {self.state_file}!")
                if user_id:
                    print(f"👤 ID de usuario real de MakerWorld: {user_id}")
                    self._update_user_id_in_config(user_id)
                self._send_telegram_alert(
                    f"🎉 <b>¡Sesión de MakerWorld iniciada con éxito!</b>\n\n"
                    f"👤 Cuenta: <code>{email}</code>\n"
                    f"🆔 Usuario: <code>{user_id or 'Detectado'}</code>\n\n"
                    f"A partir de ahora, el bot puede publicar y consultar estadísticas de forma 100% autónoma."
                )
                browser.close()
                return True
            else:
                try:
                    debug_path = self.base_dir / "output" / "login_failed_state.png"
                    page.screenshot(path=str(debug_path))
                    print(f"Captura de estado guardada en {debug_path}")
                except Exception:
                    pass
                browser.close()
                print("❌ No se pudo completar el inicio de sesión.")
                return False

    def ensure_valid_session(self) -> bool:
        """Ensures that a valid session exists. If not, runs direct_login automatically."""
        if self.has_saved_session():
            return True
        return self.direct_login()

    def launch_interactive_login(self) -> bool:
        """Alias for direct_login."""
        return self.direct_login()
