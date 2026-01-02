"""
Inventory/Products Page Object Model
Contains all elements and actions for the products page
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Inventory page object"""
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test^='remove']")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    # Dynamic locators
    def get_product_name_locator(self, product_name: str):
        """Get locator for specific product name"""
        return (By.XPATH, f"//div[@class='inventory_item_name' and text()='{product_name}']")
    
    def get_add_to_cart_button_by_name(self, product_name: str):
        """Get add to cart button for specific product"""
        product_id = product_name.lower().replace(' ', '-')
        return (By.ID, f"add-to-cart-{product_id}")
    
    def __init__(self, driver):
        """Initialize inventory page"""
        super().__init__(driver)
        
    def is_inventory_page_loaded(self) -> bool:
        """
        Check if inventory page is loaded
        
        Returns:
            True if loaded, False otherwise
        """
        try:
            return self.get_text(self.PAGE_TITLE) == "Products"
        except:
            return False
            
    def get_page_title(self) -> str:
        """
        Get page title
        
        Returns:
            Page title text
        """
        return self.get_text(self.PAGE_TITLE)
        
    def get_product_count(self) -> int:
        """
        Get number of products displayed
        
        Returns:
            Product count
        """
        products = self.find_elements(self.INVENTORY_ITEMS)
        count = len(products)
        logger.info(f"Product count: {count}")
        return count
        
    def add_product_to_cart(self, product_name: str):
        """
        Add product to cart by name
        
        Args:
            product_name: Name of the product
        """
        locator = self.get_add_to_cart_button_by_name(product_name)
        self.click(locator)
        logger.info(f"Added product to cart: {product_name}")
        
    def add_first_product_to_cart(self):
        """Add first product to cart"""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
        if buttons:
            buttons[0].click()
            logger.info("Added first product to cart")
            
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart
        
        Returns:
            Cart item count
        """
        try:
            count = int(self.get_text(self.SHOPPING_CART_BADGE))
            logger.info(f"Cart item count: {count}")
            return count
        except:
            logger.info("Cart is empty")
            return 0
            
    def click_shopping_cart(self):
        """Click shopping cart icon"""
        self.click(self.SHOPPING_CART_LINK)
        logger.info("Clicked shopping cart")
        
    def sort_products(self, sort_option: str):
        """
        Sort products
        
        Args:
            sort_option: Sort option (Name (A to Z), Name (Z to A), Price (low to high), Price (high to low))
        """
        self.select_dropdown_by_text(self.PRODUCT_SORT_DROPDOWN, sort_option)
        logger.info(f"Sorted products: {sort_option}")
        
    def open_menu(self):
        """Open burger menu"""
        self.click(self.BURGER_MENU)
        logger.info("Opened menu")
        
    def logout(self):
        """Logout from application (assumes menu is already open)"""
        self.wait_for_element_visible(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
        logger.info("Logged out")
