Feature: Conservation status scheme management
    Scenario: List conservation status schemes
        Given A set of conservation status schemes
        | Scheme |
        | BOCC5  |

        When I navigate to the conservation status schemes page
        Then There will be 1 scheme in the schemes list

    Scenario: Add conservation status scheme
        Given I navigate to the conservation status schemes page
        When I click on the "Add Conservation Status Scheme" button
        And I enter the conservation status scheme name
        | Scheme |
        | BOCC5  |

        And I click on the "Add Conservation Status Scheme" button
        Then There will be 1 scheme in the schemes list

    Scenario: Add a conservation status rating
        Given A set of conservation status schemes
        | Scheme |
        | BOCC5  |

        When I navigate to the conservation status schemes page
        And I click on the "edit" icon
        And I click on the "Add Status Rating" button
        Then I am taken to the "Add Conservation Status Rating" page

        When I enter the conservation status rating name
        | Rating |
        | Red    |

        And I click on the "Add Conservation Status Rating" button
        Then There will be 1 rating in the ratings list
