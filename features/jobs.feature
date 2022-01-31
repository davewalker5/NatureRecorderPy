Feature: Background job management
    Scenario: View recent background jobs
        Given The jobs list is empty
        And I have started a sightings export
        When I navigate to the job list page
        Then There will be 1 job in the jobs list
