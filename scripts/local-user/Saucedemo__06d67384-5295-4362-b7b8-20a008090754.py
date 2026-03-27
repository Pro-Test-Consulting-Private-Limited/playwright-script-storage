import re
import sys
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1500)
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()

    page.set_default_timeout(3000)

    def highlight_and_wait(selector):
        page.evaluate(
            """(sel) => {
                const el = document.querySelector(sel);
                if (!el) return;
                el.style.outline = '4px solid red';
                el.scrollIntoView({ block: 'center' });
            }""",
            selector
        )
        page.wait_for_timeout(800)


    original_locator = page.locator

    def custom_locator(selector, *args, **kwargs):
        highlight_and_wait(selector)
        return original_locator(selector, *args, **kwargs)

    page.locator = custom_locator

    try:
        page.goto("https://www.saucedemo.com/")
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("standard_user")
        page.locator("[data-test=\"password\"]").click()
        page.locator("[data-test=\"password\"]").fill("secret_sauce")
        page.locator("[data-test=\"password\"]").press("Enter")
        page.locator("[data-test=\"login-button\"]").click()
        page.get_by_role("button", name="Open Menu").click()
        page.get_by_role("button", name="Close Menu").click()
    except Exception as e:
        # Capture failure screenshot
        try:
            if page and not page.is_closed():
                page.screenshot(path="failure.png", full_page=True)
        except:
            pass

        print(e)
        sys.exit(1)

    finally:
        try: 
            context.close()
        except:
            pass
        
        try:
            browser.close()
        except:
            pass


with sync_playwright() as playwright:
    run(playwright)
