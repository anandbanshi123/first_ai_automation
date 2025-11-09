from .base_page import BasePage
from ..utils.locators import ProductPageLocators

class ProductPage(BasePage):
    def add_to_cart(self):
        self.click(ProductPageLocators.ADD_TO_CART_BUTTON)

    def get_product_info(self):
        product_name = self.get_text(ProductPageLocators.PRODUCT_NAME)
        product_price = self.get_text(ProductPageLocators.PRODUCT_PRICE)
        return {
            "name": product_name,
            "price": product_price
        }
    
    