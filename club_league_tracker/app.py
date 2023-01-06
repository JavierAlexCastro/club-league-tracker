import os
import json

from flask import Flask, render_template, request, url_for, redirect
from club_league_tracker.db import db_session, create_db
from club_league_tracker.service import db_service

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
create_db()
app.app_context().push()

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
        return redirect(url_for('site_home')) # DISABLES CLUB SEARCH
        # TODO: validate <club_tag>
        club_tag = request.form.get('club_tag')
        return redirect(
            url_for('site_club_members', input_club_tag=str(club_tag)))

    return render_template('members_search.html')

@app.route('/club-members/<input_club_tag>')
def site_club_members(input_club_tag: str):
    # TODO: sanitize path param
    club_tag = input_club_tag.replace('#', '') #TODO: standardize who adds '#'
    members = []
    try:
        # TODO: proper logging
        print(f"Getting club members from DB for club {input_club_tag}")
        members = db_service.get_club_members(club_tag)
        print(f"Retrieved {str(len(members))} club_members for club {input_club_tag}")
    except Exception as ex:
        # TODO: proper logging and exception handling
        raise RuntimeError("Error getting club members") from ex

    return render_template('members.html', member_list = members)

@app.route('/member')
def show_member_details():
    query_param_key = 'tag'
    args = request.args
    raw_tag = args.get(query_param_key)
    # TODO: sanitize path param
    if raw_tag is None:
        # TODO: proper logging and exception handling
        raise ValueError(f"Invalid club member tag passed through query parameter. \
            Parameter must be {query_param_key}")

    tag = f"#{raw_tag}"
    member = None
    member_details = None
    try:
        # TODO: proper logging
        print(f"Getting member details from DB for member {tag}")
        member = db_service.get_club_member(tag)
        member_details = db_service.get_club_member_details(tag)
        print(f"Retrieved member details for member {tag}")
    except Exception as ex:
        # TODO: proper logging and exception handling
        raise RuntimeError("Error getting club member details") from ex

    current_season = None
    season_games = []
    try:
        if member is not None:
            # TODO: proper logging
            print(f"Getting club league games for the current season for {member.tag}")
            current_season = db_service.get_latest_club_league_season()
            if current_season is not None:
                season_games = db_service.get_club_league_games_for_season(current_season.id, tag)
    except Exception as ex:
        raise RuntimeError(f"Error getting season's club leage games for member {tag}")

    return render_template('member.html', member = member, member_details = member_details, cl_season_games = season_games, season = current_season)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
