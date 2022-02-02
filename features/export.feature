Feature: Export Sightings
  @export
  Scenario: Export unfiltered sightings
    Given A set of sightings
    | Date       | Location      | Category   | Species   | Number | Gender  | WithYoung |
    | 10/01/2022 | Test Location | Birds      | Blackbird | 1      | Male    | No        |
    | 01/01/2022 | Test Location | Amphibians | Frog      | 1      | Unknown | No        |

    When I navigate to the export page
    And I enter the export properties
    | Filename      | Location | Category | Species |
    | sightings.csv |          |          |         |

    And I click on the "Export Sightings" button
    Then The export starts
    And There will be 2 sightings in the export file

  @export
  Scenario: Export filtered sightings
    Given A set of sightings
    | Date       | Location      | Category   | Species   | Number | Gender  | WithYoung |
    | 10/01/2022 | Test Location | Birds      | Blackbird | 1      | Male    | No        |
    | 01/01/2022 | Test Location | Amphibians | Frog      | 1      | Unknown | No        |

    When I navigate to the export page
    And I enter the export properties
    | Filename      | Location      | Category | Species   |
    | sightings.csv | Test Location | Birds    | Blackbird |

    And I click on the "Export Sightings" button
    Then The export starts
    And There will be 1 sighting in the export file
