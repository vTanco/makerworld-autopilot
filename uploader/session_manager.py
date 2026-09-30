"""
Session and Authentication Manager for MakerWorld.
Maintains persistent browser profiles and cookies so logins survive across autonomous runs.
Equipped with Cloudflare Turnstile anti-bot bypass & Real Chrome launch support.
"""

import os
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
        print("  🌐 LAUNCHING REAL GOOGLE CHROME (CLOUDFLARE BYPASS)")
        print("=======================================================")
        print("Opening genuine Google Chrome window...")
        print("1. Log into MakerWorld (using Google, Email/Password, or Bambu Lab).")
        print("2. Once logged in and you see your avatar, return here and press ENTER.\n")

        # Launch real Chrome in isolated profile with remote debugging
        cmd = [
            str(chrome_bin),
            f"--remote-debugging-port={port}",
            f"--user-data-dir={self.profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "https://makerworld.com/en"
        ]

        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

        try:
            input(">>> Press [ENTER] in this terminal AFTER you have logged in: ")
        except EOFError:
            pass

        # Now connect via Playwright to extract the authenticated storage state
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                try:
                    browser = p.chromium.connect_over_cdp(f"http://localhost:{port}")
                    contexts = browser.contexts
                    if contexts:
                        contexts[0].storage_state(path=str(self.state_file))
                        print(f"✅ Session and cookies successfully captured to {self.state_file}!")
                    browser.close()
                except Exception as e:
                    print(f"[SessionManager] Note: Direct cookie extraction via CDP: {e}")
        except ImportError:
            pass

        # Terminate the interactive Chrome process
        try:
            proc.terminate()
        except Exception:
            pass

        return True

    def launch_interactive_login(self) -> bool:
        """
        Launches interactive login. Uses Real Chrome if available to bypass Cloudflare/Google blocks,
        falling back to Playwright Chromium with stealth anti-automation flags.
        """
        chrome_bin = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if chrome_bin.exists():
            return self.launch_real_chrome_login()

        # Fallback to Stealth Playwright Chromium
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[SessionManager] Error: Playwright is not installed.")
            return False

        print("\n=======================================================")
        print("  MAKERWORLD STEALTH AUTHENTICATION")
        print("=======================================================")
        print("Opening stealth browser. Please log into your MakerWorld account.")
        print("Tip: If using Email/Password, Cloudflare will pass automatically.")
        print("Once logged in, return here and press ENTER.\n")

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
                headless=False,
                args=stealth_args,
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 800}
            )

            # Mask navigator.webdriver
            browser.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page = browser.new_page()
            page.goto("https://makerworld.com/en")

            try:
                input(">>> Press [ENTER] once you have completed login in the browser window: ")
            except EOFError:
                pass

            browser.storage_state(path=str(self.state_file))
            browser.close()

        print(f"✅ Session successfully saved to {self.state_file}!")
        return True
