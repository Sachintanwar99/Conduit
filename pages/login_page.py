# pages/login_page.py

from pages.base_page import BasePage


class LoginPage(BasePage):
    #  Inherit from BasePage — gets click, fill, navigate etc.

    # ----------------------------------------------------------
    # SELECTORS — put what you found by inspecting the page
    # ----------------------------------------------------------
    URL            = "/login"
    EMAIL_INPUT    = "[placeholder='Email']"
    PASSWORD_INPUT = "[placeholder='Password']"
    SUBMIT_BUTTON  = "button[type='submit']"
    ERROR_MESSAGES = ".error-messages li"

    # ----------------------------------------------------------
    # ACTIONS
    # navigate() is called INSIDE a method — not in class body
    # ----------------------------------------------------------

    def open(self):
        """Navigate to the login page."""
        self.navigate(self.URL)  #  self.navigate — on the instance

    def enter_email(self, email: str):
        """Type into the email field."""
        self.fill(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Type into the password field."""
        self.fill(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the login button."""
        self.click(self.SUBMIT_BUTTON)

    def login(self, email: str, password: str):
        """
        Combined method — does all steps in one call.
        Tests use this for happy path and negative cases.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()

    # ----------------------------------------------------------
    # GETTERS — read state from the page
    # ----------------------------------------------------------

    def get_errors(self) -> list[str]:
        """Return list of all error messages shown."""
        self.wait_for_selector(self.ERROR_MESSAGES)
        return self.get_all_texts(self.ERROR_MESSAGES)

    def has_errors(self) -> bool:
        """Return True if any error message is visible."""
        return self.count(self.ERROR_MESSAGES) > 0

    def is_on_login_page(self) -> bool:
        """Return True if currently on the login page."""
        return "/login" in self.get_url()
    
    def is_submit_disabled(self) -> bool:
        # Check if the submit button is enabled and clickable.
         return self.page.locator( self.SUBMIT_BUTTON ).is_disabled()




## The Key Rules to Remember
"""
RULE 1: Always inherit from BasePage
  class LoginPage(BasePage) ✅
  class loginPage           ❌ (no inheritance, wrong naming too)

RULE 2: Never call methods in the class body
  def open(self):
      self.navigate("/login")  ✅ inside a method

  class LoginPage(BasePage):
      BasePage.navigate(...)   ❌ directly in class body

RULE 3: Always use self. to call methods
  self.navigate()  ✅
  self.fill()      ✅
  BasePage.navigate()  ❌

RULE 4: Class name is PascalCase
  LoginPage  ✅
  loginPage  ❌
"""