Feature: Reporting
    @wip
    Scenario: Report on sightings of species at a location
        Given A set of sightings
        | Date       | Location      | Category   | Species       | Number | Gender  | WithYoung |
        | TODAY      | Test Location | Birds      | Woodpigeon    | 1      | Unknown | No        |
        | TODAY      | Test Location | Birds      | Blackbird     | 1      | Male    | No        |
        | TODAY      | Test Location | Birds      | Robin         | 1      | Unknown | No        |
        | TODAY      | Test Location | Mammals    | Grey Squirrel | 1      | Unknown | No        |

        When I navigate to the location report page
        And I fill in the location report details
        | Location      | Category   | From       |
        | Test Location | Birds      | 01/01/2022 |

        # Selenium web-driver doesn't like clicking on the generate report button so the step code for the form-fill
        # step sends an ENTER after entering the from date, which submits the form instead
        # And I click on the "Generate Report" button
        Then There will be 3 results in the report table
