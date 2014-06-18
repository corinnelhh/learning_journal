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


@lettuce.step('entries containing text in markdown and plain English')
def text_with_markdown(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    lettuce.world.response = lettuce.world.client.get(home_url)

