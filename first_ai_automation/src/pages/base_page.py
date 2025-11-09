from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def __init__(self, page):
        self.page = page

    async def click(self, selector):
        await self.page.click(selector)

    async def input_text(self, selector, text):
        await self.page.fill(selector, text)

    async def wait_for_element(self, selector):
        await self.page.wait_for_selector(selector)

    async def get_text(self, selector):
        return await self.page.inner_text(selector)

    async def is_visible(self, selector):
        return await self.page.is_visible(selector)