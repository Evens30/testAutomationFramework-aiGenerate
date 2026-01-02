# 🥒 BDD Quick Start Guide

Get started with BDD testing in 5 minutes!

## What is BDD?

**Behavior-Driven Development (BDD)** lets you write tests in plain English that everyone can understand.

### Traditional Test
```python
def test_login():
    driver.get("url")
    driver.find_element(By.ID, "username").send_keys("user")
    # ... more code
```

### BDD Test
```gherkin
Scenario: Login with valid credentials
  Given I am on the login page
  When I enter username "user"
  And I enter password "password"
  And I click login
  Then I should see the dashboard
```

## Quick Setup

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Run Example Tests
```bash
# Run all BDD tests
pytest

# Run smoke tests only
pytest -m smoke

# Run with verbose output
pytest -v
```

### 3. View Reports
```bash
# HTML Report
open reports/test_report.html

# Allure Report
allure serve reports/allure-results
```

## Write Your First BDD Test

### Step 1: Create Feature File

Create `features/calculator.feature`:

```gherkin
Feature: Calculator
  As a user
  I want to perform calculations
  So that I can solve math problems

  @smoke
  Scenario: Add two numbers
    Given I have a calculator
    When I add 5 and 3
    Then the result should be 8
```

### Step 2: Create Step Definitions

Create `step_definitions/test_calculator_steps.py`:

```python
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios
scenarios('../features/calculator.feature')

# Calculator fixture
@given('I have a calculator', target_fixture='calculator')
def calculator():
    return {}

@when(parsers.parse('I add {a:d} and {b:d}'))
def add_numbers(calculator, a, b):
    calculator['result'] = a + b

@then(parsers.parse('the result should be {expected:d}'))
def verify_result(calculator, expected):
    assert calculator['result'] == expected
```

### Step 3: Run Your Test

```bash
pytest step_definitions/test_calculator_steps.py -v
```

Output:
```
test_calculator_steps.py::test_add_two_numbers PASSED [100%]
```

## Gherkin Syntax Guide

### Structure

```gherkin
Feature: Feature name
  Description

  Background: (Optional - runs before each scenario)
    Given common setup

  Scenario: Scenario name
    Given precondition
    When action
    Then expected result

  Scenario Outline: Template scenario
    Given I have <item>
    When I use <action>
    Then I should see <result>

    Examples:
      | item  | action | result |
      | apple | eat    | full   |
```

### Keywords

- **Feature** - High-level description
- **Scenario** - Test case
- **Given** - Initial context
- **When** - Action/event
- **Then** - Expected outcome
- **And/But** - Additional steps
- **Background** - Common setup
- **Scenario Outline** - Template
- **Examples** - Test data

### Tags

```gherkin
@smoke @critical
Scenario: Important test
  ...

@regression @slow
Scenario: Full test
  ...
```

Run tagged tests:
```bash
pytest -m smoke
pytest -m "smoke and critical"
pytest -m "not slow"
```

## Common Step Patterns

### Navigation
```gherkin
Given I am on the login page
Given I navigate to "https://example.com"
```

### Input
```gherkin
When I enter username "john"
When I type "hello" in the search box
When I select "Option 1" from dropdown
```

### Actions
```gherkin
When I click the login button
When I submit the form
When I press Enter
```

### Verification
```gherkin
Then I should see "Welcome"
Then the title should be "Dashboard"
Then I should be on the products page
```

## Step Definition Patterns

### Simple Step
```python
@given('I am on the login page')
def navigate_to_login(driver):
    driver.get("https://example.com/login")
```

### Parametrized Step
```python
@when(parsers.parse('I enter username "{username}"'))
def enter_username(driver, username):
    driver.find_element(By.ID, "user").send_keys(username)
```

### With Return Value
```python
@given('I have a user', target_fixture='user')
def create_user():
    return {"name": "John", "role": "admin"}
```

## Using Page Objects

```python
from pages.login_page import LoginPage

@given('I am on the login page', target_fixture='login_page')
def navigate_to_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    return login_page

@when(parsers.parse('I login as "{username}"'))
def perform_login(login_page, username):
    login_page.login(username, "password")
```

## Best Practices

### Feature Files
✅ **DO:**
- Use descriptive names
- Write user stories
- Keep scenarios focused
- Use tags for organization

❌ **DON'T:**
- Write implementation details
- Make scenarios too long
- Repeat scenarios
- Use technical jargon

### Step Definitions
✅ **DO:**
- Reuse steps across scenarios
- Keep steps simple
- Use page objects
- Add proper assertions

❌ **DON'T:**
- Duplicate step code
- Put logic in features
- Hardcode test data
- Ignore failures

## Example: Complete BDD Test

### Feature File
```gherkin
Feature: Shopping Cart
  As a customer
  I want to add items to cart
  So that I can purchase them

  Background:
    Given I am logged in as "customer"

  @smoke
  Scenario: Add single item
    When I add "Widget" to cart
    Then cart should contain 1 item

  @regression
  Scenario Outline: Add multiple items
    When I add "<item>" to cart
    Then cart should contain <count> items

    Examples:
      | item   | count |
      | Widget | 1     |
      | Gadget | 2     |
```

### Step Definitions
```python
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/shopping.feature')

@given(parsers.parse('I am logged in as "{role}"'))
def login_user(driver, role):
    # Login implementation
    pass

@when(parsers.parse('I add "{item}" to cart'))
def add_to_cart(driver, item):
    # Add to cart implementation
    pass

@then(parsers.parse('cart should contain {count:d} item'))
@then(parsers.parse('cart should contain {count:d} items'))
def verify_cart_count(driver, count):
    # Verify cart count
    assert True  # Replace with actual check
```

## Running in CI/CD

### Jenkins
```bash
# In Jenkinsfile
pytest -m smoke --alluredir=reports/allure-results
```

### Docker
```bash
docker run selenium-bdd-tests pytest -m regression
```

### GitHub Actions
```yaml
- name: Run BDD Tests
  run: |
    pip install -r requirements.txt
    pytest -m smoke
```

## Debugging Tips

### Run specific scenario
```bash
pytest -k "scenario_name"
```

### See print statements
```bash
pytest -s
```

### Stop on first failure
```bash
pytest -x
```

### Verbose output
```bash
pytest -vv
```

### Show local variables
```bash
pytest -l
```

## Next Steps

1. ✅ Run example tests
2. ✅ Read feature files in `features/`
3. ✅ Study step definitions in `step_definitions/`
4. ✅ Write your own feature
5. ✅ Create step definitions
6. ✅ Run your tests
7. ✅ View reports
8. ✅ Set up Jenkins (optional)

## Helpful Commands

```bash
# Install
pip install -r requirements.txt

# Run all
pytest

# Run smoke
pytest -m smoke

# Run parallel
pytest -n 4

# Generate report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Run in Docker
docker-compose up selenium-tests
```

## Resources

- [pytest-bdd Docs](https://pytest-bdd.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)
- [Example Features](features/)
- [Example Steps](step_definitions/)

---

**Happy BDD Testing! 🥒**
