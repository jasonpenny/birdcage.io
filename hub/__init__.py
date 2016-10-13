import os
import sqlite3

from flask import Flask, g, jsonify, request

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    DATABASE=os.path.join(app.root_path, 'hub.db'))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = connect_db()

    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

    db.close()

IntegrityError = sqlite3.IntegrityError

import hub.views
