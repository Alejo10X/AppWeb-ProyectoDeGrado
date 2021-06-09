import os
import locale

from functools import wraps
from flask import Flask, session, flash, redirect, url_for


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            flash('Sin autorización. Por favor inicia sesión', 'danger')
            return redirect(url_for('login'))

    return wrap


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', LANG='es_CO.utf8')
    locale.setlocale(locale.LC_ALL, app.config['LANG'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import home, auth, main

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    return app
