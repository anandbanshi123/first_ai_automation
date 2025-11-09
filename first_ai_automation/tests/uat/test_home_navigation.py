# first_ai_automation/tests/uat/test_home_navigation.py

import pytest
from playwright.sync_api import Page
from src.pages.home_page import HomePage

@pytest.mark.usefixtures("setup")
class TestHomeNavigation:

    def test_navigate_to_category(self, page: Page):
        home_page = HomePage(page)
        home_page.navigate_to_category("Women")
        assert page.title() == "Women - H&M"

    def test_search_for_item(self, page: Page):
        home_page = HomePage(page)
        home_page.search_for_item("Dress")
        assert "Dress" in page.title()

    def test_verify_banner_links(self, page: Page):
        home_page = HomePage(page)
        home_page.verify_banner_links()
        assert home_page.banner_links_are_valid()

    def test_navigation_elements(self, page: Page):
        home_page = HomePage(page)
        assert home_page.is_navigation_visible()
        assert home_page.is_search_bar_visible()