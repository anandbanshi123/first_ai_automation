from .base_page import BasePage
from playwright.sync_api import Page

class HomePage(BasePage):
    URL = "https://www2.hm.com/en_in/index.html"

    # simple selectors (adaptive if site updates)
    SEARCH_INPUT = 'input[type="search"], input[aria-label*="search"]'
    DISMISS_COOKIES = 'button[title*="Accept"], button:has-text("Accept"), button:has-text("OK")'

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.goto(self.URL)

    def accept_cookies(self):
        try:
            btn = self.page.query_selector(self.DISMISS_COOKIES)
            if btn:
                btn.click()
        except Exception:
            pass

    def search(self, query: str):
        el = self.page.wait_for_selector(self.SEARCH_INPUT, timeout=3000)
        el.fill(query)
        el.press("Enter")

    def navigate_to_category(self, category_name):
        category_locator = HomePageLocators.get_category_locator(category_name)
        self.click(category_locator)

    def search_for_item(self, item_name):
        self.input_text(HomePageLocators.SEARCH_INPUT, item_name)
        self.click(HomePageLocators.SEARCH_BUTTON)