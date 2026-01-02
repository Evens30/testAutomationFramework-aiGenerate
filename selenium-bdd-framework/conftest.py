"""
Pytest Configuration and Fixtures for BDD
"""

import pytest
from datetime import datetime
from utils.driver_manager import DriverManager
from utils.screenshot_manager import ScreenshotManager
from utils.logger import setup_logger
from config.settings import TestConfig, REPORTS_DIR
import json
import os

logger = setup_logger(__name__)

# Store test results for custom reporting
test_results = []


@pytest.fixture(scope="function")
def driver():
    """
    WebDriver fixture
    Creates driver instance for each test
    """
    logger.info("Setting up WebDriver")
    driver = DriverManager.get_driver()
    
    yield driver
    
    logger.info("Tearing down WebDriver")
    DriverManager.quit_driver(driver)


@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """
    Test logger fixture
    Logs test start and end
    """
    test_name = request.node.name
    logger.info(f"{'='*80}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'='*80}")
    
    yield
    
    logger.info(f"{'='*80}")
    logger.info(f"Finished test: {test_name}")
    logger.info(f"{'='*80}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    # Capture screenshot on failure
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            test_name = item.name
            screenshot_path = ScreenshotManager.capture_screenshot_on_failure(driver, test_name)
            
            # Attach screenshot to Allure report
            if screenshot_path:
                try:
                    import allure
                    allure.attach.file(
                        screenshot_path,
                        name=f"failure_screenshot_{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass
                    
                # Attach to HTML report
                if hasattr(report, 'extra'):
                    report.extra = getattr(report, 'extra', [])
                    report.extra.append(pytest.html.extras.image(screenshot_path))
    
    # Store test result
    if report.when == 'call':
        test_result = {
            'name': item.name,
            'outcome': report.outcome,
            'duration': report.duration,
            'timestamp': datetime.now().isoformat(),
            'feature': _get_feature_name(item),
            'tags': _get_tags(item)
        }
        test_results.append(test_result)


def _get_feature_name(item):
    """Extract feature name from test item"""
    try:
        # For BDD tests
        if hasattr(item, 'callspec'):
            return item.callspec.params.get('feature_name', 'Unknown')
        # Try to get from file path
        if 'features' in str(item.fspath):
            return str(item.fspath).split('/')[-1].replace('.feature', '')
    except:
        pass
    return 'Unknown'


def _get_tags(item):
    """Extract tags from test item"""
    tags = []
    for marker in item.iter_markers():
        tags.append(marker.name)
    return tags


def pytest_configure(config):
    """
    Pytest configuration hook
    """
    # Set custom metadata
    config._metadata = {
        'Project': 'Selenium BDD Test Automation Framework',
        'Tester': 'Automation Team',
        'Environment': TestConfig.ENVIRONMENT,
        'Base URL': TestConfig.BASE_URL,
        'Framework': 'pytest-bdd',
        'Python': os.sys.version.split()[0]
    }
    
    # Configure HTML report
    config.option.htmlpath = str(REPORTS_DIR / 'test_report.html')
    config.option.self_contained_html = True


def pytest_html_report_title(report):
    """
    Customize HTML report title
    """
    from config.settings import ReportConfig
    report.title = ReportConfig.REPORT_TITLE + ' - BDD Tests'


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown():
    """
    Session level setup and teardown
    """
    logger.info("="*100)
    logger.info("BDD TEST SESSION STARTED")
    logger.info(f"Environment: {TestConfig.ENVIRONMENT}")
    logger.info(f"Base URL: {TestConfig.BASE_URL}")
    logger.info("="*100)
    
    yield
    
    logger.info("="*100)
    logger.info("BDD TEST SESSION COMPLETED")
    logger.info("="*100)
    
    # Save test results to JSON
    results_file = REPORTS_DIR / 'bdd_test_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'total_tests': len(test_results),
            'passed': len([r for r in test_results if r['outcome'] == 'passed']),
            'failed': len([r for r in test_results if r['outcome'] == 'failed']),
            'tests': test_results
        }, f, indent=4)
    logger.info(f"BDD test results saved to: {results_file}")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection
    Add markers based on test tags from Gherkin
    """
    for item in items:
        # BDD tests already have markers from @tags in feature files
        # Add additional markers if needed
        if "login" in item.nodeid.lower():
            if not any(marker.name == 'login' for marker in item.iter_markers()):
                item.add_marker(pytest.mark.login)


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    Hook called before each BDD scenario
    """
    logger.info(f"Starting Scenario: {scenario.name}")


def pytest_bdd_after_scenario(request, feature, scenario):
    """
    Hook called after each BDD scenario
    """
    logger.info(f"Completed Scenario: {scenario.name}")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    Hook called when a step fails
    """
    logger.error(f"Step failed: {step.name}")
    logger.error(f"Exception: {exception}")
