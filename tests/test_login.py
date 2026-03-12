import pytest

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