Feature: Product Inventory
  As a logged in user
  I want to view and manage products
  So that I can shop for items

  Background:
    Given I am logged in as "standard_user" with password "secret_sauce"

  @smoke @critical
  Scenario: View products on inventory page
    Then I should see the products page
    And the page title should be "Products"
    And I should see at least 1 product displayed

  @smoke
  Scenario: Add single product to cart
    When I add the first product to cart
    Then the cart badge should show 1 item

  @regression
  Scenario: Add multiple products to cart
    When I add product "sauce-labs-backpack" to cart
    And I add product "sauce-labs-bike-light" to cart
    Then the cart badge should show 2 items

  @regression
  Scenario: Sort products by name A to Z
    When I sort products by "Name (A to Z)"
    Then I should see products displayed

  @regression
  Scenario: Sort products by name Z to A
    When I sort products by "Name (Z to A)"
    Then I should see products displayed

  @regression
  Scenario: Sort products by price low to high
    When I sort products by "Price (low to high)"
    Then I should see products displayed

  @regression
  Scenario: Sort products by price high to low
    When I sort products by "Price (high to low)"
    Then I should see products displayed

  @smoke
  Scenario: Navigate to shopping cart
    When I add the first product to cart
    And I click the shopping cart icon
    Then I should be on the cart page

  @smoke @critical
  Scenario: Logout from application
    When I open the menu
    And I click logout
    Then I should be redirected to the login page

  @regression
  Scenario Outline: Add specific products to cart
    When I add product "<product_name>" to cart
    Then the cart badge should show <count> item

    Examples:
      | product_name           | count |
      | sauce-labs-backpack    | 1     |
      | sauce-labs-bike-light  | 1     |
      | sauce-labs-bolt-t-shirt| 1     |
