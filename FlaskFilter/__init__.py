import os
from flask import Flask
from flask_cors import CORS
import weapon_definitions as wd
from pyqt_gui import MHDatabaseWindow as mhdb

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

from FlaskFilter import views
from FlaskFilter import admin_views

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # CORS(app, resources)
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

    return app
