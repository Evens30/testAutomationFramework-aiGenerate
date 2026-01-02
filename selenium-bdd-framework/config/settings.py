"""
Configuration settings for the test framework
"""

import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up to project root
REPORTS_DIR = BASE_DIR / 'reports'
SCREENSHOTS_DIR = REPORTS_DIR / 'screenshots'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = REPORTS_DIR / 'logs'

# Create directories if they don't exist
for directory in [REPORTS_DIR, SCREENSHOTS_DIR, DATA_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Browser Settings
class BrowserConfig:
    BROWSER = os.getenv('BROWSER', 'chrome')  # chrome, firefox, edge
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    WINDOW_SIZE = os.getenv('WINDOW_SIZE', '1920,1080')
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))

# Test Settings
class TestConfig:
    BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')
    PARALLEL_TESTS = int(os.getenv('PARALLEL_TESTS', '1'))
    RERUN_FAILURES = int(os.getenv('RERUN_FAILURES', '1'))
    
# Report Settings
class ReportConfig:
    REPORT_TITLE = 'Test Automation Report'
    REPORT_NAME = 'test_report.html'
    ALLURE_RESULTS_DIR = str(REPORTS_DIR / 'allure-results')
    
# Logging Settings
class LogConfig:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = str(LOGS_DIR / 'test_execution.log')

# Test Data
class TestData:
    VALID_USERNAME = 'standard_user'
    VALID_PASSWORD = 'secret_sauce'
    LOCKED_USERNAME = 'locked_out_user'
    INVALID_USERNAME = 'invalid_user'
    INVALID_PASSWORD = 'invalid_password'
