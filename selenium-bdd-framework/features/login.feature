Feature: User Login
  As a user
  I want to login to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @smoke @critical
  Scenario: Successful login with valid credentials
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the products page
    And the page title should be "Products"

  @regression
  Scenario: Login with invalid username
    When I enter username "invalid_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username and password do not match"

  @regression
  Scenario: Login with invalid password
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username and password do not match"

  @regression
  Scenario: Login with empty username
    When I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username is required"

  @regression
  Scenario: Login with empty password
    When I enter username "standard_user"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Password is required"

  @regression
  Scenario: Login with locked out user
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "locked out"

  @smoke
  Scenario Outline: Login with different user types
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should be on the "<expected_page>" page

    Examples:
      | username        | password     | expected_page |
      | standard_user   | secret_sauce | products      |
      | problem_user    | secret_sauce | products      |
      | performance_glitch_user | secret_sauce | products |
