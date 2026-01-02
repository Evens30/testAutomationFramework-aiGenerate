"""
WebDriver Manager Utility
Handles driver initialization and teardown
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.settings import BrowserConfig
import logging

logger = logging.getLogger(__name__)


class DriverManager:
    """WebDriver Manager class"""
    
    @staticmethod
    def get_driver():
        """
        Initialize and return WebDriver based on configuration
        
        Returns:
            WebDriver instance
        """
        browser = BrowserConfig.BROWSER.lower()
        
        logger.info(f"Initializing {browser} driver")
        
        if browser == 'chrome':
            return DriverManager._get_chrome_driver()
        elif browser == 'firefox':
            return DriverManager._get_firefox_driver()
        elif browser == 'edge':
            return DriverManager._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
            
    @staticmethod
    def _get_chrome_driver():
        """
        Get Chrome WebDriver
        
        Returns:
            Chrome WebDriver instance
        """
        options = webdriver.ChromeOptions()
        
        # Add common options
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Add headless mode if configured
        if BrowserConfig.HEADLESS:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            width, height = BrowserConfig.WINDOW_SIZE.split(',')
            options.add_argument(f'--window-size={width},{height}')
            
        # Add experimental options
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        DriverManager._configure_driver(driver)
        logger.info("Chrome driver initialized successfully")
        return driver
        
    @staticmethod
    def _get_firefox_driver():
        """
        Get Firefox WebDriver
        
        Returns:
            Firefox WebDriver instance
        """
        options = webdriver.FirefoxOptions()
        
        # Add headless mode if configured
        if BrowserConfig.HEADLESS:
            options.add_argument('--headless')
            
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        driver.maximize_window()
        DriverManager._configure_driver(driver)
        logger.info("Firefox driver initialized successfully")
        return driver
        
    @staticmethod
    def _get_edge_driver():
        """
        Get Edge WebDriver
        
        Returns:
            Edge WebDriver instance
        """
        options = webdriver.EdgeOptions()
        
        # Add headless mode if configured
        if BrowserConfig.HEADLESS:
            options.add_argument('--headless')
            
        options.add_argument('--start-maximized')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        DriverManager._configure_driver(driver)
        logger.info("Edge driver initialized successfully")
        return driver
        
    @staticmethod
    def _configure_driver(driver):
        """
        Configure driver with common settings
        
        Args:
            driver: WebDriver instance
        """
        driver.implicitly_wait(BrowserConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(BrowserConfig.PAGE_LOAD_TIMEOUT)
        logger.info("Driver configured with timeouts")
        
    @staticmethod
    def quit_driver(driver):
        """
        Quit driver safely
        
        Args:
            driver: WebDriver instance
        """
        if driver:
            try:
                driver.quit()
                logger.info("Driver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting driver: {e}")
