"""
Step definitions for Inventory feature
"""

from pytest_bdd import given, when, then, parsers, scenarios
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import TestConfig
import allure

# Load all scenarios from inventory.feature
scenarios('../features/inventory.feature')


@given(parsers.parse('I am logged in as "{username}" with password "{password}"'), target_fixture='inventory_page')
def login_user(driver, username, password):
    """Login user before inventory tests"""
    with allure.step(f"Login as {username}"):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page(TestConfig.BASE_URL)
        login_page.login(username, password)
        
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_inventory_page_loaded(), "Failed to login"
        return inventory_page


@then('I should see the products page')
def verify_products_page(inventory_page):
    """Verify products page is displayed"""
    with allure.step("Verify products page is displayed"):
        assert inventory_page.is_inventory_page_loaded(), "Products page not displayed"


@then(parsers.parse('the page title should be "{title}"'))
def verify_page_title(inventory_page, title):
    """Verify page title"""
    with allure.step(f"Verify page title is '{title}'"):
        actual_title = inventory_page.get_page_title()
        assert actual_title == title, f"Expected title '{title}', got '{actual_title}'"


@then(parsers.parse('I should see at least {count:d} product displayed'))
def verify_product_count(inventory_page, count):
    """Verify minimum product count"""
    with allure.step(f"Verify at least {count} product(s) displayed"):
        product_count = inventory_page.get_product_count()
        assert product_count >= count, f"Expected at least {count} products, got {product_count}"


@when('I add the first product to cart')
def add_first_product(inventory_page):
    """Add first product to cart"""
    with allure.step("Add first product to cart"):
        inventory_page.add_first_product_to_cart()


@when(parsers.parse('I add product "{product_name}" to cart'))
def add_specific_product(inventory_page, product_name):
    """Add specific product to cart"""
    with allure.step(f"Add product '{product_name}' to cart"):
        inventory_page.add_product_to_cart(product_name)


@then(parsers.parse('the cart badge should show {count:d} item'))
@then(parsers.parse('the cart badge should show {count:d} items'))
def verify_cart_count(inventory_page, count):
    """Verify cart item count"""
    with allure.step(f"Verify cart has {count} item(s)"):
        cart_count = inventory_page.get_cart_item_count()
        assert cart_count == count, f"Expected {count} items in cart, got {cart_count}"


@when(parsers.parse('I sort products by "{sort_option}"'))
def sort_products(inventory_page, sort_option):
    """Sort products"""
    with allure.step(f"Sort products by '{sort_option}'"):
        inventory_page.sort_products(sort_option)


@then('I should see products displayed')
def verify_products_displayed(inventory_page):
    """Verify products are displayed after action"""
    with allure.step("Verify products are displayed"):
        product_count = inventory_page.get_product_count()
        assert product_count > 0, "No products displayed"


@when('I click the shopping cart icon')
def click_shopping_cart(inventory_page):
    """Click shopping cart icon"""
    with allure.step("Click shopping cart icon"):
        inventory_page.click_shopping_cart()


@then('I should be on the cart page')
def verify_cart_page(driver):
    """Verify user is on cart page"""
    with allure.step("Verify on cart page"):
        current_url = driver.current_url
        assert "cart.html" in current_url, f"Not on cart page. Current URL: {current_url}"


@when('I open the menu')
def open_menu(inventory_page):
    """Open burger menu"""
    with allure.step("Open menu"):
        inventory_page.open_menu()


@when('I click logout')
def click_logout(inventory_page):
    """Click logout"""
    with allure.step("Click logout"):
        inventory_page.logout()


@then('I should be redirected to the login page')
def verify_login_page_redirect(driver):
    """Verify redirect to login page"""
    with allure.step("Verify redirect to login page"):
        login_page = LoginPage(driver)
        assert login_page.is_login_page_loaded(), "Not redirected to login page"
