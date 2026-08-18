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
from playwright.sync_api import Playwright, sync_playwright, Locator


# ============================================================
# ORIGINAL PLAYWRIGHT METHODS
# ============================================================

_original_click = Locator.click
_original_fill = Locator.fill
_original_check = Locator.check
_original_uncheck = Locator.uncheck
_original_select_option = Locator.select_option
_original_press = Locator.press


# ============================================================
# HIGHLIGHT
# ============================================================

def highlight(locator):
    try:
        # IMPORTANT:
        # Wait until Playwright can actually resolve the element.
        locator.wait_for(state="visible", timeout=10000)

        # Scroll it into the center.
        locator.scroll_into_view_if_needed()

        # Apply highlight.
        locator.evaluate("""
            el => {
                el.dataset.__pw_old_outline = el.style.outline || "";
                el.dataset.__pw_old_outline_offset =
                    el.style.outlineOffset || "";

                el.style.setProperty(
                    "outline",
                    "5px solid red",
                    "important"
                );

                el.style.setProperty(
                    "outline-offset",
                    "3px",
                    "important"
                );

                el.style.setProperty(
                    "background-color",
                    "rgba(255, 255, 0, 0.25)",
                    "important"
                );
            }
        """)

        # Give the browser time to render the highlight.
        locator.page.wait_for_timeout(1000)

    except Exception as e:
        print(f"[HIGHLIGHT ERROR] {e}")


def remove_highlight(locator):
    try:
        locator.evaluate("""
            el => {
                el.style.outline =
                    el.dataset.__pw_old_outline || "";

                el.style.outlineOffset =
                    el.dataset.__pw_old_outline_offset || "";

                el.style.removeProperty("background-color");

                delete el.dataset.__pw_old_outline;
                delete el.dataset.__pw_old_outline_offset;
            }
        """)
    except Exception:
        pass


# ============================================================
# PATCH CLICK
# ============================================================

def highlighted_click(self, *args, **kwargs):

    print("🔥 CLICK")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_click(self, *args, **kwargs)
    finally:
        remove_highlight(self)


# ============================================================
# PATCH FILL
# ============================================================

def highlighted_fill(self, value, *args, **kwargs):

    print("✏️ FILL")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_fill(
            self,
            value,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# ============================================================
# PATCH CHECK
# ============================================================

def highlighted_check(self, *args, **kwargs):

    print("☑️ CHECK")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_check(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# ============================================================
# PATCH UNCHECK
# ============================================================

def highlighted_uncheck(self, *args, **kwargs):

    print("☐ UNCHECK")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_uncheck(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# ============================================================
# PATCH SELECT OPTION
# ============================================================

def highlighted_select_option(self, *args, **kwargs):

    print("🔽 SELECT")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_select_option(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# ============================================================
# PATCH PRESS
# ============================================================

def highlighted_press(self, *args, **kwargs):

    print("⌨️ PRESS")
    print("   locator:", self)

    highlight(self)

    try:
        return _original_press(
            self,
            *args,
            **kwargs
        )
    finally:
        remove_highlight(self)


# ============================================================
# INSTALL PATCHES
# ============================================================

Locator.click = highlighted_click
Locator.fill = highlighted_fill
Locator.check = highlighted_check
Locator.uncheck = highlighted_uncheck
Locator.select_option = highlighted_select_option
Locator.press = highlighted_press


# ============================================================
# TEST
# ============================================================

def run(playwright: Playwright):

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=1500
    )

    context = browser.new_context(
        record_video_dir="videos/"
    )

    page = context.new_page()

    page.set_default_timeout(10000)

    try:

        print("🌐 Opening page...")

        page.goto(
            "https://ai-hub-demo.protestcorp.com/login",
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("✅ Page loaded")
        print("TITLE:", page.title())
        print("URL:", page.url)

        # Give Next.js / React hydration time to finish.
        page.wait_for_timeout(2000)

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        email = page.get_by_role(
            "textbox",
            name="you@example.com"
        )

        email.click()
        email.fill("Wrong Number")

        password = page.get_by_role(
            "textbox",
            name="••••••••"
        )

        password.click()
        password.fill("Sai@2003")

        page.get_by_role(
            "button",
            name="Show"
        ).click()

        page.get_by_role(
            "button",
            name="Login"
        ).click()

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

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

        print("✅ TEST COMPLETED")

    except Exception as e:

        print("\n❌ TEST FAILED")
        print(e)

        try:
            if not page.is_closed():
                page.screenshot(
                    path="failure.png",
                    full_page=True
                )
                print("📸 Screenshot: failure.png")
        except Exception:
            pass

        raise

    finally:

        try:
            context.close()
        except Exception:
            pass

        try:
            browser.close()
        except Exception:
            pass


with sync_playwright() as playwright:
    run(playwright)

