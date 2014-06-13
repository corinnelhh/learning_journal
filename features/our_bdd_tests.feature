Feature: My Learning Journal
    Allow for editing of the journal

    Scenario: Edit an already saved entry
        Given a saved entry
        When I click on edit
        Then a new window opens for me to edit the entry

    Scenario: Use markdown in my posts
        Given a post using markdown
        When I look at the post
        Then I see the markdown rendered 

    Scenario: Use colorized text in code blocks
        Given a post containing code
        When I look at the post
        Then I see pigmented text