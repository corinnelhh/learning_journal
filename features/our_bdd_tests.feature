Feature: My Learning Journal
    Allow for editing of the journal

    Scenario: Edit an already saved entry
        Given a database entry with the ID of 1
        When I call get_single_entry
        Then I get a dict with an ID of 1
