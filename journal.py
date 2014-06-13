# -*- coding: utf-8 -*-
import os
import datetime
import psycopg2
import markdown
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from flask import Flask, g, render_template, abort
from flask import request, url_for, redirect, session
from contextlib import closing
from passlib.hash import pbkdf2_sha256


DB_SCHEMA = """
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id serial PRIMARY KEY,
    title VARCHAR (127) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL
)
"""

DB_ENTRY_INSERT = """
INSERT INTO entries (title, text, created) VALUES (%s, %s, %s)
"""

DB_ENTRIES_LIST = """
SELECT id, title, text, created FROM entries ORDER BY created DESC
"""

DB_RETURN_BY_ID = """
SELECT id, title, text, created FROM entries WHERE id = (%s)
"""

DB_UPDATE_ENTRY = """
UPDATE entries
SET title = %s,
    text = %s,
    created = %s
WHERE id = %s
"""

app = Flask(__name__)
app.config.from_object('config')


def connect_db():
    """ Return a connection to the configured database """
    return psycopg2.connect(app.config['DATABASE'])


def init_db():
    """Initialize the database using DB_SCHEMA

    WARNING: executing this function will drop existing tables.
    """
    with closing(connect_db()) as db:
        db.cursor().execute(DB_SCHEMA)
        db.commit()


def get_database_connection():
    """ Returns a database connection """
    db = getattr(g, 'db', None)
    if db is None:
        g.db = db = connect_db()
    return db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        if exception and isinstance(exception, psycopg2.Error):
            db.rollback()
        else:
            db.commit()
        db.close()


def do_login(username='', passwd=''):
    if username != app.config['ADMIN_USERNAME']:
        raise ValueError
    if not pbkdf2_sha256.verify(passwd, app.config['ADMIN_PASSWORD']):
        raise ValueError
    session['logged_in'] = True


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            do_login(request.form['username'].encode('utf-8'),
                     request.form['password'].encode('utf-8'))
        except ValueError:
            error = "Login Failed"
        else:
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_entries'))


def write_entry(title, text):
    if not title or not text:
        raise ValueError("Title and text required for writing an entry")
    con = get_database_connection()
    cur = con.cursor()
    now = datetime.datetime.utcnow()
    cur.execute(DB_ENTRY_INSERT, [title, text, now])


def update_entry(id, title, text):
    con = get_database_connection()
    cur = con.cursor()
    now = datetime.datetime.utcnow()
    cur.execute(DB_UPDATE_ENTRY, [title, text, now, id])


def get_all_entries():
    """return a list of all entries as dicts"""
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(DB_ENTRIES_LIST)
    keys = ('id', 'title', 'text', 'created')
    rows = cur.fetchall()
    fixed = []
    for row in rows:
        fixed_row = []
        for idx, val in enumerate(row):
            if idx in (1, 2):
                val = val.decode('UTF-8')
            fixed_row.append(val)
        fixed.append(fixed_row)
    return [dict(zip(keys, row)) for row in fixed]


def get_single_entry(id):
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(DB_RETURN_BY_ID, [id])
    keys = ('id', 'title', 'text', 'created')
    rows = cur.fetchall()
    fixed = []
    for row in rows:
        fixed_row = []
        for idx, val in enumerate(row):
            if idx in (1, 2):
                val = val.decode('UTF-8')
            fixed_row.append(val)
        fixed.append(fixed_row)
    return [dict(zip(keys, row)) for row in fixed]


@app.route('/')
def show_entries():
    entries = get_all_entries()
    for entry in entries:
        entry["text"] = markdown.markdown(entry["text"])
    return render_template('list_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    try:
        write_entry(request.form['title'], request.form['text'])
    except psycopg2.Error:
        abort(500)
    return redirect(url_for('show_entries'))


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    if 'logged_in' in session:
        if request.method == 'GET':
            entry = get_single_entry(id)
        else:
            try:
                update_entry(id, request.form['title'], request.form['text'])
                return redirect(url_for('show_entries'))
            except psycopg2.Error:
                abort(500)
        return render_template('edit.html', entry=entry)
    else:
        return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
