import lettuce

from flask import url_for
from journal import app, init_db
from test_journal import clear_db, TEST_DSN
from splinter import Browser

@lettuce.before.all
def setup_app():
    print "Database  initialized."
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True

    init_db()


@lettuce.after.all
def teardown_app(total):
    print "Database cleared."
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
        with client.session_transaction() as sess:
            sess['logged_in'] = False
        lettuce.world.client = client


@lettuce.step('any text')
def random_text(step):
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
    lettuce.world.text = \
        'This is the first line of text.\n\n     `code samples here`'


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
    msg = " 'edit' button not in %s"
    assert 'class="edit-post-btn btn btn-danger btn-sm"' in body, msg % body


@lettuce.step('I do not see a button to edit posts')
def do_not_see_edit_button(step):
    body = lettuce.world.response.data
    msg = " 'edit' button in %s"
    assert 'class="edit-post-btn btn btn-danger btn-sm"' not in body, msg % body


@lettuce.step("I append '/edit/1' to the home url")
def append_edit_to_url(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    lettuce.world.response = lettuce.world.client.get(home_url + "/edit/1")


@lettuce.step('I do not see the edit entry form')
def do_not_see_edit_entry_form(step):
    body = lettuce.world.response.data
    msg = '"text": "This is my sample text." in %s'
    assert '"text": "This is my sample text."' not in body, msg % body


@lettuce.step('I see my updated entry')
def see_updated_entry(step):
    body = lettuce.world.response.data
    for val in [lettuce.world.title, lettuce.world.text]:
        assert val in body


@lettuce.step('I see my code highlighted in color')
def see_highlighted_code(step):
    body = lettuce.world.response.data
    msg = '<div class="codehilite"> not in %s'
    assert '<div class="codehilite">' in body, msg % body


@lettuce.step('I see plain text that is not code')
def do_not_see_colorized_English_text(step):
    body = "".join(lettuce.world.response.data.split())
    msg = '<divclass="entry_body"><p>Thisisthefirstlineoftext.</p> not in %s'
    assert '<divclass="entry_body"><p>Thisisthefirstlineoftext.</p>'\
        in body, msg % body
    msg2 = '<divclass="codehilite"><p>Thisisthefirstlineoftext.</p> not in %s'
    assert '<divclass="codehilite"><p>Thisisthefirstlineoftext.</p>'\
        not in body, msg2 % body


@lettuce.step('I click on the edit button')
def click_on_edit_button(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    edit_url = 'http://localhost' + home_url + "/edit/1"
    lettuce.world.response = lettuce.world.client.get(edit_url)


@lettuce.step('I see the edit entry form')
def see_edit_entry_form(step):
    body = lettuce.world.response.data
    msg = '"text": "This is my sample text." not in %s'
    assert '"text": "This is my sample text."' in body, msg % body


@lettuce.step('I see a button to tweet each post')
def see_twitter_button(step):
    body = lettuce.world.response.data
    msg = "'Tweet' button not in %s"
    assert 'class="twitter-share-button"' in body, msg % body

