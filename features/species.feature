Feature: Species management

    Scenario: List species when there are some species in the database
        Given A set of species
        | Category   | Species  |
        | Birds      | Red Kite |
        | Amphibians | Frog     |

        When I navigate to the species list page
        And I select "Birds" as the "category"
        And I click on the "List Species" button
        Then There will be 1 species in the species list

    Scenario: List species when there are none in the database
        Given A set of categories
        | Category |
        | Birds |

        And There are no "species" in the database
        When I navigate to the species list page
        And I select "Birds" as the "category"
        And I click on the "List Species" button
        Then The species list will be empty

    Scenario: Add a species
        Given A set of categories
        | Category |
        | Birds    |

        When I navigate to the species list page
        And I click on the "Add Species" button
        And  I fill in the Species details
        | Category | Species     |
        | Birds    | Sparrowhawk |

        And I click on the "Add Species" button
        And I navigate to the species list page
        And I select "Birds" as the "category"
        And I click on the "List Species" button
        Then There will be 1 species in the species list
