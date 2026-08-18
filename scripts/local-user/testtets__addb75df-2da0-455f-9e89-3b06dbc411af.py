from playwright.sync_api import Playwright, sync_playwright, Locator


def install_highlighting():

    original_click = Locator.click
    original_fill = Locator.fill

    def highlighted_click(self, *args, **kwargs):

        print("🔥 CLICK:", self)

        self.wait_for(state="visible")

        self.scroll_into_view_if_needed()

        self.evaluate("""
            el => {
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
            }
        """)

        self.page.wait_for_timeout(1000)

        return original_click(
            self,
            *args,
            **kwargs
        )

    def highlighted_fill(self, value, *args, **kwargs):

        print("✏️ FILL:", self)

        self.wait_for(state="visible")

        self.scroll_into_view_if_needed()

        self.evaluate("""
            el => {
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
            }
        """)

        self.page.wait_for_timeout(1000)

        return original_fill(
            self,
            value,
            *args,
            **kwargs
        )

    Locator.click = highlighted_click
    Locator.fill = highlighted_fill


def run(playwright: Playwright):

    # ---------------------------------------------
    # IMPORTANT: launch first
    # ---------------------------------------------

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=1500
    )

    context = browser.new_context(
        record_video_dir="videos/"
    )

    page = context.new_page()

    page.set_default_timeout(10000)

    # ---------------------------------------------
    # IMPORTANT: navigate BEFORE installing patch
    # ---------------------------------------------

    page.goto(
        "https://ai-hub-demo.protestcorp.com/login",
        wait_until="domcontentloaded",
        timeout=30000
    )

    print("PAGE:", page.url)

    page.wait_for_timeout(2000)

    # ---------------------------------------------
    # NOW install highlighting
    # ---------------------------------------------

    install_highlighting()

    # ---------------------------------------------
    # Generated Playwright code
    # ---------------------------------------------

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

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
