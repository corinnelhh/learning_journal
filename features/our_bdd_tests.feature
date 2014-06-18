Feature: My Learning Journal
    Allow for editing of the journal

    Scenario: Logged-in users can see 'edit' button
        Given a logged-in user
        When I view the home page
        Then I see a button to edit posts

     Scenario: Anonymous users cannot edit posts
        Given an anonymous user
        When I view the home page
        Then I do not see a button to edit posts

    Scenario: Logged-in users can edit posts
        Given a logged-in user
        When I click on the edit button
        Then I am redirected to the edit entry form

    Scenario: Anonymous users cannot see edit form
        Given an anonymous user
        When I append /edit to the home url
        Then I do not see the edit entry form

    Scenario: Logged-in users can save edited posts
        Given a logged-in user
        When I submit the edit form
        Then I am redirected to the home page
        And I see my updated entry

    Scenario: Users can input text with syntax colorization on code
        Given a text containing markdown
        When I look at the homepage
        Then I see only my code highlighted in color

    Scenario: Users do not see non-code in color
        Given a text in English
        When I look at the homepage
        Then I do not see colorized text
