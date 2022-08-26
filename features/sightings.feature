Feature: Sightings Management
    Scenario: List today's sightings
        Given A set of sightings
        | Date       | Location      | Category   | Species       | Number | Gender  | WithYoung | Notes      |
        | TODAY      | Test Location | Birds      | Blackbird     | 1      | Male    | No        | Some notes |
        | TODAY      | Test Location | Mammals    | Grey Squirrel | 1      | Unknown | No        | More notes |

        When I navigate to the sightings page
        Then There will be 2 sightings in the sightings list

    Scenario: List filtered sightings
        Given A set of sightings
        | Date       | Location      | Category   | Species       | Number | Gender  | WithYoung | Notes      |
        | TODAY      | Test Location | Birds      | Blackbird     | 1      | Male    | No        | Some notes |
        | TODAY      | Test Location | Mammals    | Grey Squirrel | 1      | Unknown | No        | More notes |

        When I navigate to the sightings page
        And I fill in the sightings filter form
        | Location      | Category | Species       |
        | Test Location | Mammals  | Grey Squirrel |

        And I click on the "Filter Sightings" button
        Then There will be 1 sighting in the sightings list

    Scenario: List today's sightings when there are none
        Given There are no "sightings" in the database
        When I navigate to the sightings page
        Then The sightings list will be empty

    Scenario: Create sighting
        Given A set of locations
        | Name              | Address     | City    | County      | Postcode | Country        | Latitude | Longitude |
        | Farmoor Reservoir | Cumnor Road | Farmoor | Oxfordshire | OX2 9NS  | United Kingdom | 51.75800 | -1.34752  |

        And A set of categories
        | Category |
        | Birds    |

        And A set of species
        | Category   | Species           |
        | Birds      | Black-Headed Gull |

        When I navigate to the sightings entry page
        And I fill in the sighting details
        | Date       | Location          | Category   | Species           | Number | Gender  | WithYoung |
        | TODAY      | Farmoor Reservoir | Birds      | Black-Headed Gull | 1      | Unknown | No        |

        And I click on the "Add Sighting" button
        Then The sighting will be added to the database
