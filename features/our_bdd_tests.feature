Feature: My Learning Journal
    Allow for editing of the journal

    Scenario: Edit an already saved entry
        Given a saved entry
        When I click on edit
        Then a new window opens for me to edit the entry