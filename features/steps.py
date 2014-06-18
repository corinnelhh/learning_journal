import lettuce

from flask import url_for
from journal import app, init_db
from test_journal import clear_db, TEST_DSN


@lettuce.before.all
def setup_app():
    print "This happens before all the lettuce tests begin"
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True

    init_db()


@lettuce.after.all
def teardown_app(total):
    print "This happens after all the lettuce tests have run"
    clear_db()


@lettuce.step('a logged-in user')
def logged_in_user(step):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
        lettuce.world.client = client


@lettuce.step('an anonymous user')
def anonymous_user(step):
    with app.test_client() as client:
        lettuce.world.client = client


@lettuce.step('any text')
def text_with_markdown_and_prose(step):
    lettuce.world.text = "This is my sample text."


@lettuce.step('an existing entry')
def existing_entry(step):
    lettuce.world.title = "My Title"
    entry_data = {
        'title': lettuce.world.title,
        'text': lettuce.world.text,
    }
    lettuce.world.response = lettuce.world.client.post(
        '/add', data=entry_data, follow_redirects=False
    )


@lettuce.step('text containing markdown and plain English')
def text_with_markdown_and_prose(step):
    lettuce.world.text = 'This is the first line of text.\n\n     `code samples here`'


@lettuce.step('I submit the edit form')
def edit_entry(step):
    lettuce.world.title = "My Title"

    entry_data = {
        'title': lettuce.world.title,
        'text': lettuce.world.text,
    }
    lettuce.world.response = lettuce.world.client.post(
        '/edit', data=entry_data, follow_redirects=False
    )


@lettuce.step('I view the home page')
def view_the_homepage(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    lettuce.world.response = lettuce.world.client.get(home_url)


@lettuce.step('I see a button to edit posts')
def see_edit_button(step):
    body = lettuce.world.response.data
    msg = " 'edit' button in %s"
    assert '<a href="edit/1">Edit</a>' in body, msg % body
    assert 'class="edit-links"' in body, msg % body


@lettuce.step('I do not see a button to edit posts')
def do_not_see_edit_button(step):
    body = lettuce.world.response.data
    msg = " 'edit' button in %s"
    assert '<a href="edit/1">Edit</a>' not in body, msg % body
    assert 'class="edit-links"' not in body, msg % body


@lettuce.step('I am redirected to the home page')
def redirected_home(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    # assert that we have been redirected to the home page
    assert lettuce.world.response.status_code in [301, 302]
    assert lettuce.world.response.location == 'http://localhost' + home_url
    # now, fetch the homepage so we can finish this off.
    lettuce.world.response = lettuce.world.client.get(home_url)
