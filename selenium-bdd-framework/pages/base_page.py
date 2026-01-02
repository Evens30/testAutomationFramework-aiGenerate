"""
Base Page Object Model class
All page objects inherit from this base class
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, List
import logging
from config.settings import BrowserConfig

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, BrowserConfig.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
        
    def find_element(self, locator: Tuple[str, str]):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            WebElement
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
            
    def find_elements(self, locator: Tuple[str, str]) -> List:
        """
        Find multiple elements
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Elements found: {locator}, count: {len(elements)}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
            
    def click(self, locator: Tuple[str, str]):
        """
        Click on element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked element: {locator}")
        
    def type_text(self, locator: Tuple[str, str], text: str):
        """
        Type text into input field
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Text to type
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Typed text into element: {locator}")
        
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            Text content of element
        """
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Got text from element: {locator}, text: {text}")
        return text
        
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"Got attribute '{attribute}' from element: {locator}, value: {value}")
        return value
        
    def is_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is displayed
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            True if displayed, False otherwise
        """
        try:
            element = self.find_element(locator)
            displayed = element.is_displayed()
            logger.info(f"Element displayed: {locator}, result: {displayed}")
            return displayed
        except (TimeoutException, NoSuchElementException):
            logger.info(f"Element not displayed: {locator}")
            return False
            
    def is_enabled(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is enabled
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            True if enabled, False otherwise
        """
        element = self.find_element(locator)
        enabled = element.is_enabled()
        logger.info(f"Element enabled: {locator}, result: {enabled}")
        return enabled
        
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None):
        """
        Wait for element to be visible
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Custom timeout (optional)
        """
        wait_time = timeout if timeout else BrowserConfig.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.visibility_of_element_located(locator))
        logger.info(f"Element became visible: {locator}")
        
    def wait_for_element_invisible(self, locator: Tuple[str, str], timeout: int = None):
        """
        Wait for element to be invisible
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Custom timeout (optional)
        """
        wait_time = timeout if timeout else BrowserConfig.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.invisibility_of_element_located(locator))
        logger.info(f"Element became invisible: {locator}")
        
    def scroll_to_element(self, locator: Tuple[str, str]):
        """
        Scroll to element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"Scrolled to element: {locator}")
        
    def hover_over_element(self, locator: Tuple[str, str]):
        """
        Hover over element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
        """
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
        logger.info(f"Hovered over element: {locator}")
        
    def select_dropdown_by_text(self, locator: Tuple[str, str], text: str):
        """
        Select dropdown option by visible text
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Visible text to select
        """
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.info(f"Selected dropdown option: {locator}, text: {text}")
        
    def get_page_title(self) -> str:
        """
        Get page title
        
        Returns:
            Page title
        """
        title = self.driver.title
        logger.info(f"Page title: {title}")
        return title
        
    def get_current_url(self) -> str:
        """
        Get current URL
        
        Returns:
            Current URL
        """
        url = self.driver.current_url
        logger.info(f"Current URL: {url}")
        return url
        
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        logger.info("Page refreshed")
        
    def go_back(self):
        """Navigate back"""
        self.driver.back()
        logger.info("Navigated back")
        
    def go_forward(self):
        """Navigate forward"""
        self.driver.forward()
        logger.info("Navigated forward")
        
    def switch_to_frame(self, locator: Tuple[str, str]):
        """
        Switch to iframe
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        logger.info(f"Switched to frame: {locator}")
        
    def switch_to_default_content(self):
        """Switch back to default content"""
        self.driver.switch_to.default_content()
        logger.info("Switched to default content")
        
    def accept_alert(self):
        """Accept alert dialog"""
        alert = self.driver.switch_to.alert
        alert.accept()
        logger.info("Alert accepted")
        
    def dismiss_alert(self):
        """Dismiss alert dialog"""
        alert = self.driver.switch_to.alert
        alert.dismiss()
        logger.info("Alert dismissed")
        
    def get_alert_text(self) -> str:
        """
        Get alert text
        
        Returns:
            Alert text
        """
        alert = self.driver.switch_to.alert
        text = alert.text
        logger.info(f"Alert text: {text}")
        return text
