import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
profile_dir = BASE_DIR / "data" / "browser_profile"
profile_dir.mkdir(parents=True, exist_ok=True)
state_file = profile_dir / "storage_state.json"

email = "vtancoagua@educacion.navarra.es"
password = "Vt23011995"

print("Starting direct login test...")

stealth_args = [
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--no-sandbox",
    "--no-first-run",
    "--no-default-browser-check"
]

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=False,
        args=stealth_args,
        ignore_default_args=["--enable-automation"],
        viewport={"width": 1400, "height": 900}
    )

    page = browser.new_page()
    page.goto("https://makerworld.com/es/sign-in/service?cb=https%3A%2F%2Fmakerworld.com%2Fmy%2Fmodels%2Fpublish", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    
    page.screenshot(path=str(BASE_DIR / "output" / "login_step1_loaded.png"))
    print(f"Page loaded: {page.url}")

    # Fill email
    email_input = page.locator("input[placeholder*='correo'], input[type='text'], input[type='email']").first
    if email_input.count() > 0:
        email_input.fill(email)
        print("Email filled")
    else:
        print("Email input NOT found")

    # Fill password
    pass_input = page.locator("input[type='password']").first
    if pass_input.count() > 0:
        pass_input.fill(password)
        print("Password filled")
    else:
        print("Password input NOT found")

    # Check terms checkbox
    checkbox = page.locator("input[type='checkbox']").first
    if checkbox.count() > 0:
        checkbox.check(force=True)
        print("Checkbox checked")
    else:
        print("Checkbox NOT found")

    time.sleep(1)
    page.screenshot(path=str(BASE_DIR / "output" / "login_step2_filled.png"))

    # Click Iniciar sesión
    submit_btn = page.locator("button:has-text('Iniciar sesión')").first
    if submit_btn.count() > 0:
        submit_btn.click()
        print("Submit button clicked")
    else:
        print("Submit button NOT found")

    # Wait and check what happens
    print("Waiting for response after submit...")
    for i in range(15):
        time.sleep(2)
        print(f"[{i+1}/15] Current URL: {page.url}")
        page.screenshot(path=str(BASE_DIR / "output" / f"login_step3_wait_{i}.png"))
        if "sign-in" not in page.url and "login" not in page.url:
            print("Successfully redirected away from sign-in!")
            break

    time.sleep(3)
    final_url = page.url
    print(f"Final URL: {final_url}")
    page.screenshot(path=str(BASE_DIR / "output" / "login_final.png"))

    # Save state
    browser.storage_state(path=str(state_file))
    print(f"Saved storage state to {state_file}")
    browser.close()
