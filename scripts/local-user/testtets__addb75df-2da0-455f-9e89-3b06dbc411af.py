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



import sys
from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import Locator


# ============================================================
# HIGHLIGHTER
# ============================================================

def highlight_locator(locator: Locator, page):
    try:
        # Scroll the element into the center of the viewport
        locator.scroll_into_view_if_needed()

        # Highlight the actual DOM element represented by the Locator
        locator.evaluate(
            """
            element => {
                // Save original styles so we can restore them later
                element.dataset.playwrightOriginalOutline =
                    element.style.outline || '';

                element.dataset.playwrightOriginalOutlineOffset =
                    element.style.outlineOffset || '';

                element.style.outline = '4px solid red';
                element.style.outlineOffset = '3px';

                // Make the highlight visually obvious
                element.style.transition = 'outline 0.15s ease';
            }
            """
        )

        # Keep the highlight visible
        page.wait_for_timeout(800)

    except Exception as e:
        print(f"[Highlight warning] {e}")


def remove_highlight(locator: Locator):
    try:
        locator.evaluate(
            """
            element => {
                element.style.outline =
                    element.dataset.playwrightOriginalOutline || '';

                element.style.outlineOffset =
                    element.dataset.playwrightOriginalOutlineOffset || '';

                delete element.dataset.playwrightOriginalOutline;
                delete element.dataset.playwrightOriginalOutlineOffset;
            }
            """
        )
    except Exception:
        pass


# ============================================================
# PATCH PLAYWRIGHT LOCATOR METHODS
# ============================================================

_original_click = Locator.click
_original_fill = Locator.fill
_original_check = Locator.check
_original_uncheck = Locator.uncheck
_original_select_option = Locator.select_option
_original_press = Locator.press


def highlighted_click(self, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_click(self, *args, **kwargs)
    finally:
        remove_highlight(self)


def highlighted_fill(self, value, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_fill(
            self,
            value,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


def highlighted_check(self, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_check(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


def highlighted_uncheck(self, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_uncheck(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


def highlighted_select_option(self, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_select_option(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


def highlighted_press(self, *args, **kwargs):
    page = self.page

    highlight_locator(self, page)

    try:
        return _original_press(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# Install our patched methods
Locator.click = highlighted_click
Locator.fill = highlighted_fill
Locator.check = highlighted_check
Locator.uncheck = highlighted_uncheck
Locator.select_option = highlighted_select_option
Locator.press = highlighted_press


# ============================================================
# YOUR TEST
# ============================================================

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=1500
    )

    context = browser.new_context(
        record_video_dir="videos/"
    )

    page = context.new_page()

    page.set_default_timeout(3000)

    try:

        page.goto(
            "https://ai-hub-demo.protestcorp.com/login"
        )

        page.get_by_role(
            "textbox",
            name="you@example.com"
        ).click()

        page.get_by_role(
            "textbox",
            name="you@example.com"
        ).fill(
            "Wrong Number"
        )

        page.get_by_role(
            "textbox",
            name="••••••••"
        ).click()

        page.get_by_role(
            "textbox",
            name="••••••••"
        ).fill(
            "Sai@2003"
        )

        page.get_by_role(
            "button",
            name="Show"
        ).click()

        page.get_by_role(
            "button",
            name="Login"
        ).click()

        page.get_by_role(
            "link",
            name="Approvals"
        ).click()

        page.get_by_role(
            "link",
            name="Users"
        ).click()

        page.get_by_role(
            "link",
            name="History"
        ).click()

        page.get_by_role(
            "button",
            name="Export CSV"
        ).click()

    except Exception as e:

        try:
            if page and not page.is_closed():
                page.screenshot(
                    path="failure.png",
                    full_page=True
                )
        except Exception:
            pass

        print(e)
        sys.exit(1)

    finally:

        try:
            context.close()
        except Exception:
            pass

        try:
            browser.close()
        except Exception:
            pass


# ============================================================
# START
# ============================================================

with sync_playwright() as playwright:
    run(playwright)
