# from email.policy import default
# import sqlite3
# import click
# from flask import current_app, g

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db


# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# def create_db(app):
#     default_str_val: str = 'unknown'
#     default_int_val: int = 0

#     db = SQLAlchemy(app)

#     class club_member(db.Model):
#         tag = db.Column('member_tag', db.String(16), primary_key=True)
#         name = db.Column('member_name', db.String(32), nullable=False, default='unknown')
#         role = db.Column('member_role', db.String(32), nullable=False, default='unknown')
#         trophies = db.Column('member_trophies', db.Integer, nullable=False, default=0)
#         club_league_games = db.relationship('club_league_games', backref='club_member', lazy=True)
    
#         def __repr__(self):
#             return f"Club Member:" \
#                     "|  tag({self.tag})" \
#                     "|  name({self.name}" \
#                     "|  role({self.role})" \
#                     "|  trophies({self.trophies}))"

#     class club_league_season(db.Model):
#         id = db.Column('season_id', db.Integer, nullable=False, primary_key=True)
#         week = db.Column('season_week', db.String(16), nullable=False, default='unknown')
#         start_members = db.Column('season_start_members', db.Integer, nullable=True, default=default_int_val)
#         end_members = db.Column('season_end_members', db.Integer, nullable=True, default=default_int_val)
#         day_one_trophies = db.Column('season_day_one_trophies', db.Integer, nullable=False, default=default_int_val)
#         day_two_trophies = db.Column('season_day_two_trophies', db.Integer, nullable=False, default=default_int_val)
#         day_three_trophies = db.Column('season_day_three_trophies', db.Integer, nullable=False, default=default_int_val)
#         total_trophies = db.Column('season_total_trophies', db.Integer, nullable=False, default=default_int_val)
#         participation = db.Column('season_participation', db.Integer, nullable=True, default=default_int_val)
#         is_current = db.Column('season_is_current', db.Boolean, nullable=False)
#         club_league_games = db.relationship('club_league_games', backref='club_league_season', lazy=True)
    
#         def __repr__(self):
#             return f"Club League Season:" \
#                     "|  id({self.id})" \
#                     "|  week({self.week}" \
#                     "|  start_members({self.start_members})" \
#                     "|  end_members({self.end_members})" \
#                     "|  day_one_trophies({self.day_one_trophies})" \
#                     "|  day_two_trophies({self.day_two_trophies})" \
#                     "|  day_three_trophies({self.day_three_trophies})" \
#                     "|  total_trophies({self.total_trophies})" \
#                     "|  participation({self.participation})" \
#                     "|  is_current({self.is_current}))"
    
#     class club_league_games(db.Model):
#         id = db.Column('game_id', db.Integer, nullable=False, primary_key=True)
#         season_id = db.Column(db.Integer, db.ForeignKey('club_league_season.id'), nullable=False)
#         game_day = db.Column('game_day', db.String(16), nullable=False, default=default_str_val)
#         game_mode = db.Column('game_mode', db.String(64), nullable=False, default=default_str_val)
#         game_map = db.Column('game_map', db.String(64), nullable=False, default=default_str_val)
#         game_result = db.Column('game_result', db.String(16), nullable=False, default=default_str_val)
#         game_trophies = db.Column('game_trophies', db.Integer, nullable=False, default=default_int_val)
#         member_tag = db.Column(db.String(16), db.Foreign, nullable=False)
#         member_name = db.Column('game_member_name', db.String(32), nullable=False, default=default_str_val)
#         member_brawler = db.Column('game_member_brawler', db.String(32), nullable=True, default=default_str_val)

#         def __repr__(self):
#             return f"Club League Game:" \
#                     "|  id({self.id})" \
#                     "|  season_id({self.season_id}" \
#                     "|  game_day({self.game_day})" \
#                     "|  game_mode({self.game_mode})" \
#                     "|  game_map({self.game_map})" \
#                     "|  game_result({self.game_result})" \
#                     "|  game_trophies({self.game_trophies})" \
#                     "|  member_tag({self.member_tag})" \
#                     "|  member_name({self.member_name})" \
#                     "|  member_brawler({self.member_brawler}))"
