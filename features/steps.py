import lettuce

from flask import url_for
from journal import app, init_db
from test_journal import clear_db, TEST_DSN


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


@lettuce.step("I append '/edit/1' to the home url")
def append_edit_to_url(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    lettuce.world.manual_url = home_url + "/edit/1"


@lettuce.step('I do not see the edit entry form')
def do_not_see_edit_entry_form(step):
    body = lettuce.world.response.data
    msg = 'value="Edit" not in %s'
    assert 'value="Edit"' not in body, msg % body


@lettuce.step('I see my updated entry')
def see_updated_entry(step):
    body = lettuce.world.response.data
    for val in [lettuce.world.title, lettuce.world.text]:
        assert val in body


@lettuce.step('I see my code highlighted in color')
def see_highlighted_code(step):
    body = lettuce.world.response.data
    msg = '<div class="codehilite"> in %s'
    assert '<div class="codehilite">' in body, msg % body


@lettuce.step('I see plain text that is not code')
def do_not_see_colorized_English_text(step):
    body = lettuce.world.response.data
    msg = '<p>"This is the first line of text.</p>" in %s'
    assert 'This is the first line of text.' in body, msg % body


@lettuce.step('I click on the edit button')
def click_on_edit_button(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    edit_url = 'http://localhost' + home_url + "/edit/1"
    lettuce.world.response = lettuce.world.client.get(edit_url)


@lettuce.step('I see the edit entry form')
def see_edit_entry_form(step):
    body = lettuce.world.response.data
    msg = 'value="Edit" in %s'
    assert 'value="Edit"' in body, msg % body
