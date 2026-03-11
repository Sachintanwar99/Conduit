from pytest_playwright.pytest_playwright import page

from base_page import BasePage


class LoginPage(BasePage):
    
    # SELECTORS — put what you found by inspecting the page
    # ----------------------------------------------------------
    URL            = "/login"
    EMAIL_INPUT    = "input[placeholder='Email']"
    PASSWORD_INPUT = "[placeholder='Password']"
    SUBMIT_BUTTON  = "button[type='submit']"
    ERROR_MESSAGES = ".error-messages li"

    # ----------------------------------------------------------
    # ACTIONS
    # ----------------------------------------------------------


    def open(self) :
        super().navigate(self.URL)

    def enter_email(self):
        super().fill(self.EMAIL_INPUT,"sachintanwar1689@gmail.com")
    
    def enter_pass(self):
        super().fill(self.PASSWORD_INPUT,"Okas@1689")

    def sign_in_button(self):
        super().click(self.SUBMIT_BUTTON)