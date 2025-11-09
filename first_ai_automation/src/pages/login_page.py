#visit to the site click on login button and enter credentials
from playwright.sync_api import Page
from src.pages.base_page import BasePage    
class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_url = "https://www2.hm.com/en_in/member/info.html"
        self.click_login_button = '//*[@id="main-content"]/section[1]/div[2]/div/div[2]/div[2]/label[2]'
        self.username_Email = 'input[name="email"]'
        self.click_continue_button = 'button[type="submit"]'
        self.password_input = 'input[name="password"]'
        self.login_button = 'button[type="submit"]'

    def navigate_to_login(self):
        self.goto(self.login_url)

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)