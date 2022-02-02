Feature: Life List
    The life list for a category of species consists of the unique list of species in that
    category recorded in the database

    Scenario: Life list contains species
        Given A set of sightings
        | Date       | Location      | Category   | Species   | Number | Gender  | WithYoung |
        | 01/01/2022 | Test Location | Birds      | Blackbird | 1      | Male    | No        |
        | 01/01/2022 | Test Location | Amphibians | Frog      | 1      | Unknown | No        |

        When I navigate to the life list page
        And I select "Birds" as the "category"
        And I click on the "List Species" button
        Then There will be 1 species in the life list

    Scenario: Life list contains no entries
        Given A set of categories
        | Category |
        | Birds    |

        When I navigate to the life list page
        And I select "Birds" as the "category"
        And I click on the "List Species" button
        Then The life list will be empty

    @export
    Scenario: Export life list
        Given A set of sightings
        | Date       | Location      | Category   | Species   | Number | Gender  | WithYoung |
        | 10/01/2022 | Test Location | Birds      | Blackbird | 1      | Male    | No        |
        | 01/01/2022 | Test Location | Amphibians | Frog      | 1      | Unknown | No        |

        When I navigate to the export life list page
        And I enter the life list export properties
        | Filename            | Category |
        | birds_life_list.csv | Birds    |

        And I click on the "Export Life List" button
        Then The life list export starts
        And There will be 1 entry in the export file