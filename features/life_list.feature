Feature: Life List
  The life list for a category of species consists of the unique list of species in that
  category recorded in the database

  Scenario: Life list contains species
    Given A set of sightings
    | Date       | Location      | Category | Species   | Number | Gender | WithYoung |
    | 01/01/2022 | Test Location | Birds    | Blackbird | 1      | Male   | No        |

    When I navigate to the life list page
    And I select "Birds" as the "category"
    And I click on the "List Species" button
    Then There will be 1 sighting in the life list
