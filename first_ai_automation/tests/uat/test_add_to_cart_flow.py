from playwright.sync_api import Page
import pytest
from src.pages.home_page import HomePage
from src.pages.category_page import CategoryPage
from src.pages.product_page import ProductPage

@pytest.mark.usefixtures("setup")
class TestAddToCartFlow:

    def test_add_item_to_cart(self, page: Page):
        home_page = HomePage(page)
        category_page = CategoryPage(page)
        product_page = ProductPage(page)

        # Navigate to the home page
        home_page.navigate_to_home()

        # Navigate to a category
        home_page.navigate_to_category("Men")

        # Select a product from the category
        category_page.select_item("T-Shirt")

        # Add the product to the cart
        product_page.add_to_cart()

        # Verify that the cart updates correctly
        assert product_page.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, page: Page):
        home_page = HomePage(page)
        category_page = CategoryPage(page)
        product_page = ProductPage(page)

        # Navigate to the home page
        home_page.navigate_to_home()

        # Navigate to a category
        home_page.navigate_to_category("Women")

        # Select multiple products and add them to the cart
        category_page.select_item("Dress")
        product_page.add_to_cart()
        category_page.select_item("Shoes")
        product_page.add_to_cart()

        # Verify that the cart updates correctly
        assert product_page.get_cart_count() == 2

    def test_add_item_to_cart_and_verify_details(self, page: Page):
        home_page = HomePage(page)
        category_page = CategoryPage(page)
        product_page = ProductPage(page)

        # Navigate to the home page
        home_page.navigate_to_home()

        # Navigate to a category
        home_page.navigate_to_category("Kids")

        # Select a product
        category_page.select_item("Toy")

        # Add the product to the cart
        product_page.add_to_cart()

        # Verify product details in the cart
        cart_product_info = product_page.get_product_info()
        assert cart_product_info['name'] == "Toy"
        assert cart_product_info['price'] == "$20.00"  # Example price, adjust as necessary