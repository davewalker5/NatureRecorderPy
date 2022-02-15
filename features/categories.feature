Feature: Category management
    Scenario: List categories when there are some categories in the database
        Given A set of categories
        | Category |
        | Birds    |

        When I navigate to the category list page
        Then There will be 1 category in the category list

    Scenario: List categories when there are none in the database
        Given There are no "categories" in the database
        When I navigate to the category list page
        Then The category list will be empty

    Scenario: Add a category
        Given I navigate to the category list page
        When I click on the "Add Category" button
        And  I fill in the Category details
        | Category   |
        | Amphibians |

        And I click on the "Add Category" button
        Then There will be 1 category in the category list
