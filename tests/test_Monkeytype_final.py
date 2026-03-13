import time

from playwright.sync_api import sync_playwright
EMAIL = "sachin8860tanwar@gmail.com"
PASSWORD = "Sachin@9911"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=10)
    page = browser.new_page()

    # page.goto("https://monkeytype.com/login")
    page.goto("https://monkeytype.com")

    page.wait_for_timeout(2000)

    page.keyboard.press("Tab")
    page.keyboard.press("Enter")

    # page.wait_for_timeout(2000)

    # page.locator("[name='current-email']").fill(EMAIL)
    
    # page.locator("[name='current-password']").fill(PASSWORD)

    # page.get_by_role("button", name="Sign in").click()

    # page.wait_for_load_state("networkidle")

    # page.get_by_role("link", name="Monkeytype Home").click()

    # wait for words to load
    page.wait_for_selector("#words")

    # focus typing area
    page.click("body")

    while True:

        # if result screen appears stop typing
        if page.locator("#result").is_visible():
            print("Test finished")
            break

        # get active word
        word = page.locator("#words .word.active").inner_text()

        # type word
        page.keyboard.type(word)

        # press space
        page.keyboard.press(" ")
        
        

    page.pause()