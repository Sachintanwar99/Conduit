# pages/base_page.py
# ============================================================
# WHY THIS FILE EXISTS:
# All page objects (LoginPage, HomePage etc.) inherit from here.
# Raw Playwright commands live HERE — not in test files.
# ============================================================

from playwright.sync_api import Page, expect


class BasePage:

    # Base URL of the app — change this one line to switch environments
    BASE_URL = "https://demo.realworld.show/"

    def __init__(self, page: Page):
        # page = the Playwright browser object
        # stored as self.page so every method can use it
        self.page = page

    # ----------------------------------------------------------
    # NAVIGATION
    # ----------------------------------------------------------

    def navigate(self, path: str = "") -> None:
        """
        Go to a page.
        Accepts either:
          - relative path → "/login"  (adds BASE_URL automatically)
          - full URL      → "https://example.com" (uses as-is)
        """
        url = path if path.startswith("http") else f"{self.BASE_URL}{path}"
        self.page.goto(url)

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the current page <title> tag text."""
        return self.page.title()

    # ----------------------------------------------------------
    # ACTIONS
    # WHY: Wrap raw Playwright so if API changes, fix in ONE place
    # ----------------------------------------------------------

    def click(self, selector: str) -> None:
        """Click an element. Playwright auto-waits for it to be ready."""
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        """Clear a field and type text into it."""
        self.page.locator(selector).fill(text)

    def select_option(self, selector: str, value: str) -> None:
        """Select a dropdown option by value."""
        self.page.locator(selector).select_option(value)

    def press_key(self, key: str) -> None:
        """
        Press a keyboard key.
        WHY: Some UI elements (tag inputs) respond to Enter key,
        not a button click. e.g. press_key("Enter") to add a tag.
        """
        self.page.keyboard.press(key)

    # ----------------------------------------------------------
    # READING FROM PAGE
    # ----------------------------------------------------------

    def get_text(self, selector: str) -> str:
        """Get visible text of a single element."""
        return self.page.locator(selector).inner_text()

    def get_all_texts(self, selector: str) -> list[str]:
        """
        Get text from ALL matching elements.
        WHY: When a page has a LIST of items (articles, errors,
        tags), this returns all their texts at once.
        e.g. get_all_texts(".error-messages li")
          → ["email is invalid", "password is too short"]
        """
        return self.page.locator(selector).all_inner_texts()

    def get_input_value(self, selector: str) -> str:
        """
        Get what is currently typed inside an input field.
        WHY: get_text() doesn't work on input fields.
        Use this to verify what's pre-filled in a form.
        """
        return self.page.locator(selector).input_value()

    # ----------------------------------------------------------
    # VISIBILITY CHECKS
    # ----------------------------------------------------------

    def is_visible(self, selector: str) -> bool:
        """
        Check if an element is visible RIGHT NOW.
        Returns True or False immediately — does NOT wait.
        WHY: Use for conditional checks like
             "if error banner is visible, close it"
        """
        return self.page.locator(selector).is_visible()

    def count(self, selector: str) -> int:
        """
        Count how many elements match a selector.
        WHY: Used to verify list sizes.
        e.g. count(".article-preview") → 10
        """
        return self.page.locator(selector).count()

    # ----------------------------------------------------------
    # WAITING
    # WHY: UI content loads asynchronously (AJAX/dynamic).
    # Never assert immediately — wait first.
    # ----------------------------------------------------------

    def wait_for_url(self, pattern: str) -> None:
        """
        Wait until URL matches a pattern.
        WHY: After form submit, page redirects.
        Wait for the redirect BEFORE asserting anything.
        e.g. wait_for_url("**/home")
        """
        self.page.wait_for_url(pattern)

    def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        """
        Wait until an element reaches a state.
        States: "visible", "hidden", "attached", "detached"
        WHY: Dynamic content appears AFTER page load (AJAX).
        Wait for it before reading or asserting.
        """
        self.page.wait_for_selector(selector, state=state)

    def wait_for_network(self) -> None:
        """
        Wait until all network activity stops.
        WHY: After navigation, API calls happen in background.
        This ensures all data is loaded before asserting.
        """
        self.page.wait_for_load_state("networkidle")

    # ----------------------------------------------------------
    # ASSERTIONS
    # WHY: Playwright's expect() has BUILT-IN retry logic.
    # It keeps checking until timeout — much better than
    # assert is_visible() which checks only ONCE.
    # ----------------------------------------------------------

    def expect_visible(self, selector: str) -> None:
        """Assert element becomes visible (retries automatically)."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        """Assert element becomes hidden (retries automatically)."""
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, text: str) -> None:
        """Assert element contains specific text."""
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_url_contains(self, partial_url: str) -> None:
        """Assert current URL contains a substring."""
        expect(self.page).to_have_url(lambda url: partial_url in url)

    # ----------------------------------------------------------
    # SCREENSHOT
    # WHY: Used in visual tests + auto-captured on failures
    # ----------------------------------------------------------

    def take_screenshot(self, path: str) -> None:
        """Capture full page screenshot and save to path."""
        self.page.screenshot(path=path, full_page=True)

    # ----------------------------------------------------------
    # AUTH TOKEN INJECTION
    # WHY: Skip slow UI login. Write token directly to
    # localStorage — browser thinks user is already logged in.
    # Saves 2-3 seconds per test that needs authentication.
    # ----------------------------------------------------------

    def inject_auth_token(self, token: str, username: str, email: str) -> None:
        """Inject JWT token into browser localStorage."""
        self.page.goto(self.BASE_URL)
        self.page.evaluate(f"""() => {{
            localStorage.setItem('jwtToken', '{token}');
            localStorage.setItem('userInfo', JSON.stringify({{
                "email": "{email}",
                "username": "{username}",
                "token": "{token}"
            }}));
        }}""")



## Summary of What We Have
"""
navigate()          → go to a page
get_url()           → read current URL
get_title()         → read page title

click()             → click an element
fill()              → type into a field
select_option()     → choose from dropdown
press_key()         → press Enter, Tab etc.

get_text()          → read one element's text
get_all_texts()     → read all matching elements
get_input_value()   → read what's typed in input

is_visible()        → check visibility (instant)
count()             → count matching elements

wait_for_url()      → wait for redirect
wait_for_selector() → wait for element
wait_for_network()  → wait for AJAX to finish

expect_visible()    → assert visible (with retry)
expect_hidden()     → assert hidden (with retry)
expect_text()       → assert text (with retry)

take_screenshot()   → capture screenshot
inject_auth_token() → bypass UI login
"""