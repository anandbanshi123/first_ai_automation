#add positive and negative login tests
from playwright.sync_api import Page
import pytest
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage 
from appitool import test_visual_ui

@pytest.mark.usefixtures("setup")
class TestLoginToSite:
    test_visual_ui("Login Test - Valid Credentials")
    
    def test_valid_login(self, page: Page):
        login_page = LoginPage(page)
        home_page = HomePage(page)

        # Navigate to the login page
        login_page.navigate_to_login()

        # Perform login with valid credentials
        login_page.login("valid_user", "valid_password")
        # Verify successful login by checking for an element on the home page
        assert home_page.is_user_logged_in() is True