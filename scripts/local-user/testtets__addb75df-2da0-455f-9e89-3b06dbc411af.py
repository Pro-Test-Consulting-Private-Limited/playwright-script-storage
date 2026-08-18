from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://ai-hub-demo.protestcorp.com/login")

    print("OPENED:", page.title())

    page.get_by_role(
        "textbox",
        name="you@example.com"
    ).evaluate("""
        el => {
            el.style.outline = '8px solid red';
            el.style.backgroundColor = 'yellow';
        }
    """)

    print("HIGHLIGHT APPLIED")

    page.wait_for_timeout(10000)

    browser.close()
