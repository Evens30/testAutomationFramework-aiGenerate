"""
Screenshot Utility
Handles screenshot capture and management
"""

import os
from datetime import datetime
from pathlib import Path
from config.settings import SCREENSHOTS_DIR
import logging

logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Screenshot manager class"""
    
    @staticmethod
    def capture_screenshot(driver, test_name: str) -> str:
        """
        Capture screenshot
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            
        Returns:
            Path to saved screenshot
        """
        try:
            # Create timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create filename
            filename = f"{test_name}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename
            
            # Capture screenshot
            driver.save_screenshot(str(filepath))
            
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
            
    @staticmethod
    def capture_screenshot_on_failure(driver, test_name: str) -> str:
        """
        Capture screenshot on test failure
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            
        Returns:
            Path to saved screenshot
        """
        filename = f"FAILED_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        try:
            driver.save_screenshot(str(filepath))
            logger.error(f"Failure screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {e}")
            return None
            
    @staticmethod
    def cleanup_old_screenshots(days: int = 7):
        """
        Clean up screenshots older than specified days
        
        Args:
            days: Number of days to keep screenshots
        """
        try:
            current_time = datetime.now()
            for file in SCREENSHOTS_DIR.iterdir():
                if file.is_file():
                    file_age = current_time - datetime.fromtimestamp(file.stat().st_mtime)
                    if file_age.days > days:
                        file.unlink()
                        logger.info(f"Deleted old screenshot: {file}")
        except Exception as e:
            logger.error(f"Error cleaning up screenshots: {e}")
