import os
import json

from flask import Flask, render_template
from club_league_tracker.db import db
from club_league_tracker.models.db import *

# TODO: catch error check config
def load_app_config(app, env: str):
    if env is None:
        app.config.from_file("config\default.json", load=json.load)
    else:
        config_file: str = f"{env.lower()}.json"
        if os.path.exists():
            app.config.from_file(config_file, load=json.load)
        else:
            # TODO: proper logging (WARN)
            print(f"{config_file} file not found. Loading 'default' config")
            app.config.from_file("config\default.json", load=json.load)

def load_db_config(app):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

def create_app(env: str = None):
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__)

    load_app_config(app, env)
    load_db_config(app)

    # TODO: add sensitive data dynamically
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    # )

    return app


env = os.environ.get('ENV')
app = create_app(env)

db.init_app(app)
app.app_context().push()
db.create_all()

# a simple page that says hello
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/club-members')
def get_club_members():

    members = []
    try:
        members = club_member.query.all()
        print(f"Retrieved {str(len(members))} club_members: ")
    except:
        # TODO: proper logging and exception handling
        raise

    return render_template('members.html', member_list = members)