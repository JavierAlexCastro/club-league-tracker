import os
import json

from flask import Flask, render_template, request, url_for, redirect
from club_league_tracker.db import db
from club_league_tracker.service import db_service
from club_league_tracker.models.db import ClubMember
from club_league_tracker.networking.bs_clubs import get_club_members

def get_fixie_proxy():
    fixie_proxy = None
    proxy_from_config = app.config['FIXIE_URL']
    if proxy_from_config != "":
        # TODO: proper logging
        print("Using Fixie Proxy!")
        fixie_proxy = {
            "http"  : proxy_from_config,
            "https" : proxy_from_config
        }

    return fixie_proxy

# TODO: catch error check config
def load_app_config(flask_app, flask_env: str):
    if flask_env is None:
        flask_app.config.from_file(r"config/default.json", load=json.load)
    else:
        # TODO: assumes running in linux '/'. Windows uses '\'. Should not assume.
        config_file: str = f"config/{flask_env.lower()}.json"
        if os.path.exists(os.path.join(os.getcwd(), f"club_league_tracker/{config_file}")):
            flask_app.config.from_file(config_file, load=json.load)

            if flask_env == "production":
                # TODO: proper logging
                print(f"Loading {flask_env} config")
                flask_app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
                flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
                flask_app.config['BS_API_KEY'] = os.environ['BS_API_KEY']
                flask_app.config['FIXIE_URL'] = os.environ['FIXIE_URL']
        else:
            # TODO: proper logging (WARN)
            print(f"{config_file} file not found. Loading 'default' config")
            flask_app.config.from_file(r"config\default.json", load=json.load)

def load_db_config(flask_app):
    flask_app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 2,
        "pool_recycle": 300,
        "pool_use_lifo": True
    }

def create_app(flask_env: str = None):
    # app = Flask(__name__, instance_relative_config=True)
    flask_app = Flask(__name__)

    load_app_config(flask_app, flask_env)
    load_db_config(flask_app)

    # TODO: add sensitive data dynamically
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    # )

    return flask_app


env = os.environ.get('ENV')
app = create_app(env)

db.init_app(app)
app.app_context().push()
db.create_all()

fixie_proxy = get_fixie_proxy()

# a simple page that says hello
@app.route('/')
def site_home():
    return render_template('index.html')

@app.route('/about')
def site_about():
    return render_template('about.html')

@app.route('/club-members', methods=['GET', 'POST'])
def site_club_members_search():
    if request.method == 'POST':
        # TODO: validate <club_tag>
        club_tag = request.form.get('club_tag')
        do_refresh = request.form.get('do_refresh')
        return redirect(
            url_for('site_club_members', input_club_tag=str(club_tag), refresh=do_refresh))

    return render_template('members_search.html')

@app.route('/club-members/<input_club_tag>')
def site_club_members(input_club_tag: str):
    club_tag = input_club_tag.replace('#', '')
    bs_api_key = app.config['BS_API_KEY']
    members = []
    try:
        if 'refresh' in request.args and request.args['refresh'] == 'true':
            # TODO: proper logging
            print("Getting members from API")
            members = get_club_members(club_tag=f'#{club_tag}',
                                        auth_token=bs_api_key,
                                        proxies=fixie_proxy)
            db_service.save_club_members(members)
        else:
            # TODO: proper logging
            print("Getting members from DB")
            members = ClubMember.query \
                .filter(ClubMember.club_tag.endswith(club_tag)) \
                .order_by(ClubMember.trophies.desc()) \
                .all()
        print(f"Retrieved {str(len(members))} club_members: ")
    except Exception as ex:
        # TODO: proper logging and exception handling
        raise RuntimeError("Error getting club members") from ex

    return render_template('members.html', member_list = members)
