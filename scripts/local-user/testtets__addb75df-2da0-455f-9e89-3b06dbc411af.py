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
#         page.get_by_role("textbox", name="you@example.com").fill("9900776952")
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

import re
import sys
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1500)
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()

    page.set_default_timeout(3000)

    def highlight(locator):
        locator.highlight()
        page.wait_for_timeout(800)

    try:
        page.goto("https://ai-hub-demo.protestcorp.com/login")

        email_box = page.get_by_role("textbox", name="you@example.com")
        highlight(email_box)
        email_box.click()
        email_box.fill("9900776952")

        password_box = page.get_by_role("textbox", name="••••••••")
        highlight(password_box)
        password_box.click()
        password_box.fill("Sai@2003")

        show_btn = page.get_by_role("button", name="Show")
        highlight(show_btn)
        show_btn.click()

        login_btn = page.get_by_role("button", name="Login")
        highlight(login_btn)
        login_btn.click()

        approvals_link = page.get_by_role("link", name="Approvals")
        highlight(approvals_link)
        approvals_link.click()

        users_link = page.get_by_role("link", name="Users")
        highlight(users_link)
        users_link.click()

        history_link = page.get_by_role("link", name="History")
        highlight(history_link)
        history_link.click()

        export_btn = page.get_by_role("button", name="Export CSV")
        highlight(export_btn)
        export_btn.click()

    except Exception as e:
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


with sync_playwright() as playwright:
    run(playwright)
