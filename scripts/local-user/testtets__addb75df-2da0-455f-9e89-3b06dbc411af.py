# import re
# import sys
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, slow_mo=1500)
#     context = browser.new_context(record_video_dir="videos/")
#     page = context.new_page()

#     page.set_default_timeout(3000)

#     def highlight_and_wait(selector):
#         page.evaluate(
#             """(sel) => {
#                 const el = document.querySelector(sel);
#                 if (!el) return;
#                 el.style.outline = '4px solid red';
#                 el.scrollIntoView({ block: 'center' });
#             }""",
#             selector
#         )
#         page.wait_for_timeout(800)


#     original_locator = page.locator

#     def custom_locator(selector, *args, **kwargs):
#         highlight_and_wait(selector)
#         return original_locator(selector, *args, **kwargs)

#     page.locator = custom_locator

#     try:
#         page.goto("https://ai-hub-demo.protestcorp.com/login")
#         page.get_by_role("textbox", name="you@example.com").click()
#         page.get_by_role("textbox", name="you@example.com").fill("Wrong Number")
#         page.get_by_role("textbox", name="••••••••").click()
#         page.get_by_role("textbox", name="••••••••").fill("Sai@2003")
#         page.get_by_role("button", name="Show").click()
#         page.get_by_role("button", name="Login").click()
#         page.get_by_role("link", name="Approvals").click()
#         page.get_by_role("link", name="Users").click()
#         page.get_by_role("link", name="History").click()
#         page.get_by_role("button", name="Export CSV").click()
#     except Exception as e:
#         # Capture failure screenshot
#         try:
#             if page and not page.is_closed():
#                 page.screenshot(path="failure.png", full_page=True)
#         except:
#             pass

#         print(e)
#         sys.exit(1)

#     finally:
#         try: 
#             context.close()
#         except:
#             pass
        
#         try:
#             browser.close()
#         except:
#             pass


# with sync_playwright() as playwright:
#     run(playwright)

from playwright.sync_api import sync_playwright, Locator

_original_click = Locator.click

def test_click(self, *args, **kwargs):
    print("🔥 PATCHED CLICK CALLED")
    print("Locator:", self)

    self.evaluate("""
        el => {
            el.style.outline = '6px solid red';
            el.style.backgroundColor = 'yellow';
        }
    """)

    self.page.wait_for_timeout(3000)

    return _original_click(self, *args, **kwargs)

Locator.click = test_click


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://ai-hub-demo.protestcorp.com/login"
    )

    page.get_by_role(
        "textbox",
        name="you@example.com"
    ).click()

    page.wait_for_timeout(5000)

    browser.close()
