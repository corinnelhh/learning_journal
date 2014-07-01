Feature: My Learning Journal
    Allow for editing of the journal

    Scenario: Logged-in users can see 'edit' button
        Given a logged-in user
        And any text
        And an existing entry
        When I view the home page
        Then I see a button to edit posts

     Scenario: Anonymous users cannot edit posts
        Given an anonymous user
        And any text
        And an existing entry
        When I view the home page
        Then I do not see a button to edit posts

    Scenario: Logged-in users can edit posts
        Given a logged-in user
        And any text
        And an existing entry
        When I click on the edit button
        Then I see the edit entry form

    Scenario: Anonymous users cannot see edit form
        Given an anonymous user
        When I append '/edit/1' to the home url
        Then I do not see the edit entry form

    Scenario: Logged-in users can save edited posts
        Given a logged-in user
        When I submit the edit form
        Then I view the home page
        And I see my updated entry

    Scenario: Users can input text with colorized code syntax
        Given text containing markdown and plain English
        And an existing entry
        When I view the home page
        Then I see my code highlighted in color
        And I see plain text that is not code

    Scenario: All users see a button to tweet a post
        Given an anonymous user
        And any text
        And an existing entry
        When I view the home page
        Then I see a button to tweet each post

