from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()

    # open typing website
    page.goto("https://monkeytype.com/")

    # wait for page to load
    page.wait_for_timeout(3000)

    page.keyboard.press("Tab")
    page.keyboard.press("Enter")

    # click start typing / lesson button
    page.locator("text=Start").first.click()

    page.wait_for_timeout(3000)

    # locate typing input area
    typing_area = page.locator("input")

    # type automatically
    typing_area.type(
        "this is automated typing test using playwright python",
        delay=80
    )

    page.wait_for_timeout(5000)

    browser.close()