"""
Step definitions for Login feature
"""

from pytest_bdd import given, when, then, parsers, scenarios
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import TestConfig
import allure

# Load all scenarios from login.feature
scenarios('../features/login.feature')


@given('I am on the login page', target_fixture='login_page')
def navigate_to_login_page(driver):
    """Navigate to login page"""
    with allure.step("Navigate to login page"):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page(TestConfig.BASE_URL)
        assert login_page.is_login_page_loaded(), "Login page not loaded"
        return login_page


@when(parsers.parse('I enter username "{username}"'))
def enter_username(login_page, username):
    """Enter username"""
    with allure.step(f"Enter username: {username}"):
        login_page.enter_username(username)


@when(parsers.parse('I enter password "{password}"'))
def enter_password(login_page, password):
    """Enter password"""
    with allure.step("Enter password"):
        login_page.enter_password(password)


@when('I click the login button')
def click_login_button(login_page):
    """Click login button"""
    with allure.step("Click login button"):
        login_page.click_login_button()


@then('I should be redirected to the products page')
def verify_products_page(driver):
    """Verify redirect to products page"""
    with allure.step("Verify redirect to products page"):
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_inventory_page_loaded(), "Not redirected to products page"


@then(parsers.parse('the page title should be "{title}"'))
def verify_page_title(driver, title):
    """Verify page title"""
    with allure.step(f"Verify page title is '{title}'"):
        inventory_page = InventoryPage(driver)
        actual_title = inventory_page.get_page_title()
        assert actual_title == title, f"Expected '{title}', got '{actual_title}'"


@then('I should see an error message')
def verify_error_displayed(login_page):
    """Verify error message is displayed"""
    with allure.step("Verify error message is displayed"):
        assert login_page.is_error_displayed(), "Error message not displayed"


@then(parsers.parse('the error message should contain "{text}"'))
def verify_error_message_contains(login_page, text):
    """Verify error message contains specific text"""
    with allure.step(f"Verify error message contains '{text}'"):
        error_msg = login_page.get_error_message()
        assert text.lower() in error_msg.lower(), f"Expected '{text}' in '{error_msg}'"


@then(parsers.parse('I should be on the "{page_name}" page'))
def verify_on_page(driver, page_name):
    """Verify user is on specific page"""
    with allure.step(f"Verify on {page_name} page"):
        if page_name.lower() == "products":
            inventory_page = InventoryPage(driver)
            assert inventory_page.is_inventory_page_loaded(), f"Not on {page_name} page"
