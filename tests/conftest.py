

import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.login_page import LoginPage

# Load .env file so os.getenv() can read our variables
load_dotenv()


# ============================================================
# SECTION 1: ENVIRONMENT FIXTURES
# scope="session" → created ONCE for the whole test run
# WHY: These values never change between tests
# ============================================================

@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL of the app."""
    return os.getenv("BASE_URL", "https://demo.realworld.show")


@pytest.fixture(scope="session")
def credentials() -> dict:
    """
    Return login credentials from .env file.

    WHY session scope:
    Credentials never change between tests.
    No need to re-read .env file for every test.
    """
    return {
        "email":    os.getenv("TEST_EMAIL"),
        "password": os.getenv("TEST_PASSWORD"),
        "username": os.getenv("TEST_USERNAME"),
    }


# ============================================================
# SECTION 2: PAGE FIXTURES
# scope="function" → fresh object for EACH test
# WHY: Each test needs a clean browser state.
# One test logging in should NOT affect the next test.
# ============================================================

@pytest.fixture(scope="function")
def custom_page(page: Page) -> Page:
    """
    Extend the built-in Playwright `page` fixture.

    WHY we wrap it:
    We add our own setup (viewport size) on top of
    what pytest-playwright already provides.

    pytest-playwright gives us `page` for free.
    We wrap it to customize it.
    """
    page.set_viewport_size({"width": 1280, "height": 720})
    yield page
    # No manual teardown needed —
    # pytest-playwright closes the page automatically


@pytest.fixture(scope="function")
def login_page(custom_page: Page) -> LoginPage:
    """
    Return a LoginPage object ready to use.

    WHY function scope:
    Every login test needs a FRESH page.
    If Test 1 logs in and Test 2 gets the same page,
    Test 2 starts already logged in — wrong state!

    Usage in test:
        def test_something(login_page):
            login_page.open()
            login_page.login("email", "pass")
    """
    return LoginPage(custom_page)


# ============================================================
# SECTION 3: HOOKS
# Hooks are special functions pytest calls automatically
# at specific moments — not fixtures, no @pytest.fixture
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    HOOK: Auto-capture screenshot when a test FAILS.

    WHY:
    When a test fails, you want to see exactly what the
    browser looked like at the moment of failure.
    This hook fires after every test and saves a screenshot
    if the test failed — automatically, no code in tests needed.

    Screenshots saved to: screenshots/FAILED_testname.png
    """
    outcome = yield  # let the test run first
    report = outcome.get_result()

    # Only care about the actual test body (not setup/teardown)
    # Only care about failures
    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("custom_page")
        if page:
            # Build filename from test name
            safe_name = (
                item.nodeid
                .replace("/", "_")
                .replace("::", "_")
                .replace(" ", "_")
            )
            screenshot_path = f"screenshots/FAILED_{safe_name}.png"

            # Create screenshots folder if it doesn't exist
            import os
            os.makedirs("screenshots", exist_ok=True)

            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n📸 Screenshot saved: {screenshot_path}")
            except Exception:
                pass  # never let screenshot failure break the report
