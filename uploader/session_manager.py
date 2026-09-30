"""
Session and Authentication Manager for MakerWorld.
Maintains persistent browser profiles and cookies so logins survive across autonomous runs.
"""

from pathlib import Path
import os
import json
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

    def launch_interactive_login(self) -> bool:
        """
        Launches an interactive browser window for the user to log into MakerWorld once.
        Saves full session cookies and local storage for subsequent autonomous runs.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[SessionManager] Error: Playwright is not installed. Run: pip install playwright && playwright install chromium")
            return False

        print("\n=======================================================")
        print("  MAKERWORLD ONE-TIME AUTHENTICATION")
        print("=======================================================")
        print("Opening browser. Please log into your MakerWorld / Bambu Lab account.")
        print("Once you are logged in and see your user avatar, return here and press ENTER.\n")

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=False,
                viewport={"width": 1280, "height": 800},
                channel="chrome" if Path("/Applications/Google Chrome.app").exists() else None
            )

            page = browser.new_page()
            page.goto("https://makerworld.com/en")
            
            try:
                input(">>> Press [ENTER] once you have completed login in the browser window: ")
            except EOFError:
                pass

            # Save state
            browser.storage_state(path=str(self.state_file))
            browser.close()

        print(f"[SessionManager] Session successfully saved to {self.state_file}!")
        return True
