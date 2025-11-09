from playwright.sync_api import Page

class TestSearchAndFilter:
    def test_search_functionality(self, page: Page):
        page.goto("https://www2.hm.com/en_in/index.html")
        page.fill("input[placeholder='Search']", "dress")
        page.press("input[placeholder='Search']", "Enter")
        page.wait_for_selector(".product-item")
        results = page.query_selector_all(".product-item")
        assert len(results) > 0, "No search results found."

    def test_filter_functionality(self, page: Page):
        page.goto("https://www2.hm.com/en_in/index.html")
        page.fill("input[placeholder='Search']", "dress")
        page.press("input[placeholder='Search']", "Enter")
        page.wait_for_selector(".product-item")
        
        page.click("text=Filters")
        page.click("text=Size")
        page.click("text=M")
        page.click("text=Apply")
        
        page.wait_for_timeout(2000)  # Wait for the filter to apply
        filtered_results = page.query_selector_all(".product-item")
        assert len(filtered_results) > 0, "No filtered results found."