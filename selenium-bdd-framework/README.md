# 🚀 Selenium Python BDD Test Automation Framework

A comprehensive **Behavior-Driven Development (BDD)** test automation framework using **Selenium WebDriver**, **Python**, **pytest-bdd**, and **Gherkin** syntax with complete **CI/CD integration** for Jenkins.

## 📋 Table of Contents

- [Features](#features)
- [BDD with Gherkin](#bdd-with-gherkin)
- [CI/CD Integration](#cicd-integration)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Writing BDD Tests](#writing-bdd-tests)
- [Reports](#reports)
- [Jenkins Setup](#jenkins-setup)
- [Docker Support](#docker-support)

## ✨ Features

### Core Features
- ✅ **BDD with Gherkin** - Write tests in plain English
- ✅ **pytest-bdd** - Powerful BDD framework for Python
- ✅ **Page Object Model (POM)** - Clean code architecture
- ✅ **Multiple Browsers** - Chrome, Firefox, Edge
- ✅ **Parallel Execution** - Run tests faster
- ✅ **CI/CD Ready** - Jenkins integration included
- ✅ **Docker Support** - Containerized testing
- ✅ **Screenshot on Failure** - Automatic capture
- ✅ **Multiple Report Formats** - HTML, Allure, JSON

### BDD Features
- 📝 **Gherkin Syntax** - Feature files in plain language
- 🔄 **Reusable Steps** - DRY principle for step definitions
- 🏷️ **Scenario Tags** - @smoke, @regression, @critical
- 📊 **Scenario Outlines** - Data-driven testing
- 🎯 **Given-When-Then** - Clear test structure

### CI/CD Features
- 🔧 **Jenkins Pipeline** - Complete Jenkinsfile
- 🐳 **Docker Support** - Containerized execution
- 📈 **Trend Analysis** - Track test metrics
- 📧 **Notifications** - Email/Slack alerts
- ⚙️ **Parameterized Builds** - Flexible execution
- 🔄 **Scheduled Runs** - Automated execution

## 🥒 BDD with Gherkin

### What is BDD?

**Behavior-Driven Development** is a software development approach where tests are written in natural language that non-programmers can read.

### Example Feature File

```gherkin
Feature: User Login
  As a user
  I want to login to the application
  So that I can access my account

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the products page
    And the page title should be "Products"
```

### Benefits of BDD

1. **Readable by Everyone** - Business, QA, Developers
2. **Living Documentation** - Tests serve as documentation
3. **Collaboration** - Shared understanding
4. **Test Coverage** - Clear requirements
5. **Maintainability** - Easy to update

## 🔄 CI/CD Integration

### Jenkins Pipeline Features

- **Parameterized Builds** - Choose browser, environment, test suite
- **Parallel Execution** - Configurable workers
- **Automated Reports** - HTML and Allure
- **Pass/Fail Metrics** - Build status based on results
- **Artifact Archiving** - Screenshots and logs
- **Email Notifications** - Alert on failures

### Pipeline Stages

```
┌─────────────┐
│   Cleanup   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Checkout   │
└──────┬──────┘
       │
┌──────▼──────┐
│    Setup    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Run Tests  │
└──────┬──────┘
       │
┌──────▼──────┐
│   Reports   │
└──────┬──────┘
       │
┌──────▼──────┐
│   Analyze   │
└─────────────┘
```

## 📁 Project Structure

```
selenium-bdd-framework/
│
├── features/                    # Gherkin feature files
│   ├── login.feature           # Login scenarios
│   └── inventory.feature       # Inventory scenarios
│
├── step_definitions/            # Step implementations
│   ├── test_login_steps.py    # Login step definitions
│   └── test_inventory_steps.py # Inventory step definitions
│
├── pages/                       # Page Object Models
│   ├── base_page.py            # Base page class
│   ├── login_page.py           # Login page object
│   └── inventory_page.py       # Inventory page object
│
├── utils/                       # Utility modules
│   ├── driver_manager.py       # WebDriver management
│   ├── screenshot_manager.py   # Screenshot utilities
│   └── logger.py               # Logging configuration
│
├── config/                      # Configuration
│   └── settings.py             # Framework settings
│
├── reports/                     # Test reports (auto-generated)
│   ├── allure-results/         # Allure raw data
│   ├── screenshots/            # Failure screenshots
│   ├── logs/                   # Execution logs
│   └── test_report.html        # HTML report
│
├── jenkins/                     # Jenkins files
│   ├── JENKINS_SETUP.md        # Jenkins setup guide
│   └── Jenkinsfile.simple      # Simple pipeline
│
├── conftest.py                  # Pytest fixtures
├── pytest.ini                   # Pytest configuration
├── Jenkinsfile                  # Jenkins pipeline
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 📥 Installation

### 1. Prerequisites

- Python 3.8+
- pip
- Git

### 2. Clone Repository

```bash
git clone <repository-url>
cd selenium-bdd-framework
```

### 3. Create Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configuration (Optional)

```bash
cp .env.example .env
# Edit .env with your settings
```

## 🏃 Running Tests

### Run All Tests

```bash
pytest
```

### Run by Tag

```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Critical tests
pytest -m critical
```

### Run Specific Feature

```bash
# Login feature
pytest step_definitions/test_login_steps.py

# Inventory feature
pytest step_definitions/test_inventory_steps.py
```

### Run in Parallel

```bash
pytest -n 4  # 4 workers
```

### Run with Specific Browser

```bash
BROWSER=firefox pytest
```

### Run in Headless Mode

```bash
HEADLESS=True pytest
```

### Generate Allure Report

```bash
# Run tests
pytest --alluredir=reports/allure-results

# Generate and view report
allure serve reports/allure-results
```

## ✍️ Writing BDD Tests

### Step 1: Create Feature File

Create `features/new_feature.feature`:

```gherkin
Feature: New Feature
  Description of the feature

  @smoke
  Scenario: Test scenario
    Given precondition
    When action
    Then expected result
```

### Step 2: Create Step Definitions

Create `step_definitions/test_new_feature_steps.py`:

```python
from pytest_bdd import scenarios, given, when, then, parsers
import allure

scenarios('../features/new_feature.feature')

@given('precondition')
def precondition(driver):
    with allure.step("Setup precondition"):
        # Implementation
        pass

@when('action')
def perform_action(driver):
    with allure.step("Perform action"):
        # Implementation
        pass

@then('expected result')
def verify_result(driver):
    with allure.step("Verify result"):
        # Assertion
        assert True
```

### Step 3: Run Tests

```bash
pytest step_definitions/test_new_feature_steps.py -v
```

## 📊 Reports

### HTML Report

After running tests:
```bash
open reports/test_report.html
```

Features:
- Test summary
- Pass/fail counts
- Duration
- Screenshots on failure
- Environment details

### Allure Report

Generate and view:
```bash
allure serve reports/allure-results
```

Features:
- Interactive dashboard
- Test trends
- Detailed steps
- Screenshots
- Test history
- Categories
- Beautiful UI

### JSON Report

Machine-readable format:
```bash
cat reports/bdd_report.json
```

## 🔧 Jenkins Setup

### Quick Setup

1. **Install Required Plugins**
   - Pipeline
   - Git
   - HTML Publisher
   - Allure

2. **Create Pipeline Job**
   - New Item > Pipeline
   - Configure parameters
   - Point to Jenkinsfile

3. **Run Build**
   - Build with Parameters
   - Select options
   - View reports

### Detailed Guide

See [jenkins/JENKINS_SETUP.md](jenkins/JENKINS_SETUP.md) for complete setup instructions.

### Jenkins Parameters

- **BROWSER** - chrome/firefox/edge
- **ENVIRONMENT** - staging/qa/production
- **HEADLESS** - true/false
- **TEST_SUITE** - all/smoke/regression/critical
- **PARALLEL_WORKERS** - Number of workers

### Example Jenkins Build

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest -m smoke -n 4'
            }
        }
    }
}
```

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t selenium-bdd-tests .
```

### Run Tests in Docker

```bash
docker run --rm selenium-bdd-tests
```

### Using Docker Compose

```bash
# Run tests
docker-compose up selenium-tests

# With Selenium Grid
docker-compose up
```

### Docker Features

- ✅ Isolated environment
- ✅ Consistent execution
- ✅ Easy CI/CD integration
- ✅ Selenium Grid support

## 🎯 Best Practices

### Feature Files

1. **Clear Titles** - Descriptive feature names
2. **User Stories** - Follow As-a/I-want/So-that format
3. **One Feature** - One feature per file
4. **Meaningful Tags** - Use tags for organization
5. **Scenario Outlines** - For data-driven tests

### Step Definitions

1. **Reusable Steps** - Write generic steps
2. **Clear Names** - Descriptive function names
3. **Allure Steps** - Use allure.step() for clarity
4. **Assertions** - Keep in Then steps
5. **Page Objects** - Use POM pattern

### CI/CD

1. **Parallel Execution** - Use -n flag
2. **Headless Mode** - Required for CI
3. **Timeouts** - Set build timeouts
4. **Notifications** - Alert on failures
5. **Artifacts** - Archive reports

## 📈 Metrics and Reporting

### Track These Metrics

- **Pass Rate** - Target: >95%
- **Execution Time** - Monitor trends
- **Flaky Tests** - Identify and fix
- **Coverage** - Scenarios vs requirements
- **Build Success Rate** - CI/CD health

### Allure Trends

View test trends over time:
- Pass/fail history
- Duration trends
- Flaky test detection
- Category distribution

## 🐛 Troubleshooting

### Tests fail in CI but pass locally

```bash
# Solution: Use headless mode
HEADLESS=True pytest
```

### WebDriver not found

```bash
# Solution: Install webdriver-manager
pip install webdriver-manager
```

### Jenkins build fails

```bash
# Check:
# 1. Python installed
# 2. Dependencies installed
# 3. Browser available
# 4. Correct workspace path
```

## 📚 Learning Resources

- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add features/scenarios
4. Write step definitions
5. Test locally
6. Submit pull request

## 📄 License

This framework is provided for educational and testing purposes.

---

## 🎓 Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run smoke tests
pytest -m smoke

# Run with Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Run in Jenkins
# Use Jenkinsfile - see jenkins/JENKINS_SETUP.md

# Run in Docker
docker-compose up selenium-tests
```

---

**Happy BDD Testing! 🥒✨**
