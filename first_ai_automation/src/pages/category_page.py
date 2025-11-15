Import asyncio
class CategoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    async def filter_items(self, filter_criteria):
        await self.page.click(f'//button[text()="{filter_criteria}"]')
        await self.wait_for_element('//div[contains(@class, "filtered-items")]')

    async def select_item(self, item_name):
        await self.page.click(f'//a[contains(@class, "item-name") and text()="{item_name}"]')
        await self.wait_for_element('//div[contains(@class, "product-details")]')
if __name__ == "__main__":
    print("BasePage module loaded.")