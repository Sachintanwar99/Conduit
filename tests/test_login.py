import pytest

# ============================================================
# HAPPY PATH TESTS
# ============================================================

@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login_redirects_to_home(login_page, credentials):
    """
    SCENARIO: Valid user logs in with correct credentials.
    EXPECT: Redirected away from login page → home page loads.

    WHY this assertion:
    After successful login the URL changes from /login to /.
    If login failed, URL stays on /login.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login(
        credentials["email"],
        credentials["password"]
    )

    # Assert
    # Wait for redirect to complete first
    login_page.page.wait_for_url(
        "**/", timeout=10000
    )
    assert "login" not in login_page.get_url(), \
        "After valid login, URL should not contain /login"


@pytest.mark.smoke
@pytest.mark.ui
def test_login_page_loads_correctly(login_page):
    """
    SCENARIO: Open the login page.
    EXPECT: Page loads and form elements are visible.

    WHY this test:
    Most basic check — if the page doesn't even load,
    all other login tests will also fail.
    Always test the foundation first.
    """
    # Arrange + Act
    login_page.open()

    # Assert — verify form elements are visible
    assert login_page.is_visible(login_page.EMAIL_INPUT), \
        "Email input should be visible"
    assert login_page.is_visible(login_page.PASSWORD_INPUT), \
        "Password input should be visible"
    assert login_page.is_visible(login_page.SUBMIT_BUTTON), \
        "Submit button should be visible"


# ============================================================
# NEGATIVE TESTS
# WHY: Test what happens when things go WRONG.
# Negative tests are just as important as positive ones.
# ============================================================

@pytest.mark.regression
@pytest.mark.ui
def test_wrong_password_shows_error(login_page):
    """
    SCENARIO: Correct email but wrong password.
    EXPECT: Error message appears, stay on login page.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("valid@email.com", "wrongpassword")

    # Assert
    assert login_page.has_errors(), \
        "Error message should appear for wrong password"


@pytest.mark.regression
@pytest.mark.ui
def test_wrong_email_shows_error(login_page):
    """
    SCENARIO: Email that doesn't exist in the system.
    EXPECT: Error message appears.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("nobody@nowhere.com", "somepassword")

    # Assert
    assert login_page.has_errors(), \
        "Error message should appear for unregistered email"


@pytest.mark.regression
@pytest.mark.ui
def test_empty_email_shows_error(login_page):
    """
    SCENARIO: User submits form with no email.
    EXPECT: Validation error appears.

    WHY separate test from empty password:
    Each validation rule should be tested independently.
    If they're combined, you don't know which rule failed.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("", "somepassword")

    # Assert
    assert login_page.has_errors(), \
        "Error should appear when email is empty"


@pytest.mark.regression
@pytest.mark.ui
def test_empty_password_shows_error(login_page):
    """
    SCENARIO: User submits form with no password.
    EXPECT: Validation error appears.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("valid@email.com", "")

    # Assert
    assert login_page.has_errors(), \
        "Error should appear when password is empty"


@pytest.mark.regression
@pytest.mark.ui
def test_both_fields_empty_shows_error(login_page):
    """
    SCENARIO: User clicks submit without filling anything.
    EXPECT: Validation error appears.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("", "")

    # Assert
    assert login_page.has_errors(), \
        "Error should appear when both fields are empty"


@pytest.mark.regression
@pytest.mark.ui
def test_error_message_content(login_page):
    """
    SCENARIO: Wrong credentials submitted.
    EXPECT: Error message contains meaningful text.

    WHY this test:
    Previous tests only check IF error appears.
    This test checks WHAT the error says.
    Both matter — a blank error message is also a bug.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("wrong@email.com", "wrongpass")

    # Assert
    errors = login_page.get_errors()
    assert len(errors) > 0, "At least one error message should appear"

    # Join all errors into one string for easier checking
    all_errors = " ".join(errors).lower()
    assert any(word in all_errors for word in
               ["invalid", "incorrect", "wrong", "email", "password"]), \
        f"Error message should be meaningful. Got: {errors}"


# ============================================================
# PARAMETRIZE
# CONCEPT: Run the same test with multiple data sets.
# Instead of writing 3 separate functions, write one.
# pytest creates one test case per row automatically.
# ============================================================

@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("email, password", [
    ("",                  "somepassword"),   # empty email
    ("valid@email.com",   ""),              # empty password
    ("",                  ""),              # both empty
    ("notanemail",        "password123"),   # invalid email format
    ("wrong@email.com",   "wrongpass"),     # wrong credentials
])
def test_invalid_login_combinations(login_page, email, password):
    """
    PARAMETRIZED: Multiple invalid login combinations.

    WHY parametrize:
    All these scenarios expect the same result — error appears.
    Instead of 5 separate functions, one function handles all.
    pytest runs it 5 times, once per row.

    In terminal you will see:
      test_invalid_login_combinations[email0-password0]
      test_invalid_login_combinations[email1-password1]
      ... and so on
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login(email, password)

    # Assert
    assert login_page.has_errors(), \
        f"Error should appear for email='{email}' password='{password}'"


# ============================================================
# STAYING ON PAGE TESTS
# ============================================================

@pytest.mark.regression
@pytest.mark.ui
def test_failed_login_stays_on_login_page(login_page):
    """
    SCENARIO: Login fails.
    EXPECT: User stays on /login page — not redirected.

    WHY this test:
    If login fails but somehow redirects, that's a
    serious security bug. Verify URL explicitly.
    """
    # Arrange
    login_page.open()

    # Act
    login_page.login("wrong@email.com", "wrongpass")

    # Assert
    assert "login" in login_page.get_url(), \
        "Failed login should keep user on /login page"