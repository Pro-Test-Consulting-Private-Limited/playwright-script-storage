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
        page.goto("https://ai-hub-demo.protestcorp.com/login")
        page.get_by_role("button", name="Sign in with Microsoft").click()
        page.get_by_role("textbox", name="Enter your email, phone, or").click()
        page.get_by_role("textbox", name="Enter your email, phone, or").fill("vijaykumar.panchagatti@protestcorp.com")
        page.get_by_role("textbox", name="Enter your email, phone, or").press("Enter")
        page.get_by_role("button", name="Next").click()
        page.get_by_role("textbox", name="Enter the password for").click()
        page.get_by_role("textbox", name="Enter the password for").click()
        page.get_by_role("textbox", name="Enter the password for").fill("Sanjose@123")
        page.get_by_role("button", name="Sign in").click()
        page.goto("https://login.microsoftonline.com/common/SAS/ProcessAuth")
        page.get_by_role("link", name="Not now").click()
        page.get_by_role("button", name="Yes").click()
        page.get_by_role("link", name="+ Add money").click()
        page.get_by_role("spinbutton", name="500").click()
        page.get_by_role("spinbutton", name="500").fill("1000")
        page.get_by_role("button", name="Add money →").click()
        page.locator("iframe").content_frame.get_by_test_id("contactNumber").click()
        page.locator("iframe").content_frame.get_by_test_id("contactNumber").fill("9845047926")
        page.locator("iframe").content_frame.locator("[data-test-id=\"add-card-cta\"]").click()
        page.locator("iframe").content_frame.locator("span").filter(has_text="Wallet").first.click()
        page.locator("iframe").content_frame.get_by_role("button", name="Mobikwik Mobikwik").click()
        page.locator("iframe").content_frame.get_by_role("button", name="Continue").click()
        page.locator("iframe").content_frame.get_by_placeholder("Email address").click()
        page.locator("iframe").content_frame.get_by_placeholder("Email address").fill("vijaykumar.panchagatti@protestcorp.com")
        page.locator("iframe").content_frame.get_by_role("button", name="Continue").click()
        page.locator("iframe").content_frame.get_by_placeholder("Enter OTP").click()
        page.locator("iframe").content_frame.get_by_placeholder("Enter OTP").click()
        page.locator("iframe").content_frame.get_by_placeholder("Enter OTP").fill("123456")
        page.locator("iframe").content_frame.get_by_test_id("dialog-H").get_by_text("Secured by").click()
        page.locator("iframe").content_frame.get_by_role("button", name="Continue").click()
        page.get_by_text("PPro-TestQUALITY ASSUREDDashboardWalletKYCHistoryProfileLogoutFund Transfer ·").click()
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
