class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    async def get_results(self):
        return await self.page.locator("selector_for_results").all_text_contents()

    async def select_result(self, index):
        await self.page.locator(f"selector_for_results:nth-child({index})").click()
        