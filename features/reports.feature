Feature: Reporting
    Scenario: Report on numbers of individuals by location
        Given A set of sightings
        | Date       | Location      | Category   | Species       | Number | Gender  | WithYoung |
        | TODAY      | Test Location | Birds      | Woodpigeon    | 1      | Unknown | No        |
        | TODAY      | Test Location | Birds      | Blackbird     | 1      | Male    | No        |
        | TODAY      | Test Location | Birds      | Robin         | 1      | Unknown | No        |
        | TODAY      | Test Location | Mammals    | Grey Squirrel | 1      | Unknown | No        |

        When I navigate to the individuals by location report page
        And I fill in the individuals by location report details
        | Location      | Category   | From  |
        | Test Location | Birds      | TODAY |

        And I click on the "Generate Report" button
        Then There will be 3 results in the report table

    Scenario: Report on numbers of individuals by location
        Given A set of sightings
        | Date       | Location      | Category   | Species       | Number | Gender  | WithYoung |
        | TODAY      | Test Location | Birds      | Woodpigeon    | 1      | Unknown | No        |
        | TODAY      | Test Location | Mammals    | Grey Squirrel | 1      | Unknown | No        |

        When I navigate to the sightings by location report page
        And I fill in the sightings by location report details
        | Location      | Category   | From  |
        | Test Location | Birds      | TODAY |

        And I click on the "Generate Report" button
        Then There will be 1 result in the report table
