# test_product_details.py

import pytest
from playwright.sync_api import Page
from src.pages.home_page import HomePage
from src.pages.product_page import ProductPage

@pytest.mark.usefixtures("setup")
class TestProductDetails:

    def test_view_product_details(self, page: Page):
        home_page = HomePage(page)
        product_page = ProductPage(page)

        # Navigate to the home page
        home_page.navigate_to_home()

        # Search for a product
        home_page.search_for_item("T-shirt")

        # Select the first product from the search results
        product_page.select_product_from_results()

        # Verify product details
        product_info = product_page.get_product_info()
        assert product_info['name'] == "Expected Product Name"
        assert product_info['price'] == "Expected Product Price"
        assert product_info['description'] == "Expected Product Description"

    def test_product_images(self, page: Page):
        home_page = HomePage(page)
        product_page = ProductPage(page)

        # Navigate to the home page
        home_page.navigate_to_home()

        # Search for a product
        home_page.search_for_item("T-shirt")

        # Select the first product from the search results
        product_page.select_product_from_results()

        # Verify product images are displayed
        assert product_page.is_image_displayed(), "Product image is not displayed"