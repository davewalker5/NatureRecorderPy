Feature: Location management

    Scenario: List locations when there are some locations in the database
        Given A set of locations
        | Name              | Address     | City    | County      | Postcode | Country        | Latitude | Longitude |
        | Farmoor Reservoir | Cumnor Road | Farmoor | Oxfordshire | OX2 9NS  | United Kingdom | 51.75800 | -1.34752  |

        When I navigate to the locations list page
        Then There will be 1 location in the locations list

    Scenario: List locations when there are none in the database
        Given There are no "locations" in the database
        When I navigate to the locations list page
        Then The locations list will be empty

    Scenario: Add a location
        Given I navigate to the locations list page
        When I click on the "Add Location" button
        And  I fill in the location details
        | Name              | Address     | City    | County      | Postcode | Country        | Latitude | Longitude |
        | Farmoor Reservoir | Cumnor Road | Farmoor | Oxfordshire | OX2 9NS  | United Kingdom | 51.75800 | -1.34752  |

        And I click on the "Add Location" button
        Then There will be 1 location in the locations list
