"""
Login Page Object Model
Contains all elements and actions for the login page
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CLASS_NAME, "error-button")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
    
    def __init__(self, driver):
        """Initialize login page"""
        super().__init__(driver)
        
    def navigate_to_login_page(self, url: str):
        """
        Navigate to login page
        
        Args:
            url: Login page URL
        """
        self.driver.get(url)
        logger.info(f"Navigated to login page: {url}")
        
    def enter_username(self, username: str):
        """
        Enter username
        
        Args:
            username: Username to enter
        """
        self.type_text(self.USERNAME_INPUT, username)
        logger.info(f"Entered username: {username}")
        
    def enter_password(self, password: str):
        """
        Enter password
        
        Args:
            password: Password to enter
        """
        self.type_text(self.PASSWORD_INPUT, password)
        logger.info("Entered password")
        
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        logger.info("Clicked login button")
        
    def get_error_message(self) -> str:
        """
        Get error message text
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)
        
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed
        
        Returns:
            True if error is displayed, False otherwise
        """
        return self.is_displayed(self.ERROR_MESSAGE)
        
    def is_login_page_loaded(self) -> bool:
        """
        Check if login page is loaded
        
        Returns:
            True if loaded, False otherwise
        """
        return self.is_displayed(self.LOGIN_LOGO)
        
    def login(self, username: str, password: str):
        """
        Perform login action
        
        Args:
            username: Username
            password: Password
        """
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
