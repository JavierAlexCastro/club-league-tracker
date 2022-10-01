from club_league_tracker.db import db
from club_league_tracker.models.enums.defaults import Defaults

class ClubLeagueGames(db.Model):
    game_id = db.Column('game_id', db.Integer,nullable=False, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('club_league_season.season_id'), nullable=False)
    game_day = db.Column('game_day', db.String(16), nullable=False, default=Defaults.STRING)
    game_mode = db.Column('game_mode', db.String(64), nullable=False, default=Defaults.STRING)
    game_map = db.Column('game_map', db.String(64), nullable=False, default=Defaults.STRING)
    game_result = db.Column('game_result', db.String(16), nullable=False, default=Defaults.STRING)
    game_trophies = db.Column('game_trophies', db.Integer, nullable=False, default=Defaults.INTEGER)
    member_tag = db.Column(db.String(16), db.ForeignKey('club_member.member_tag'), nullable=False)
    member_name = db.Column('game_member_name', db.String(32), nullable=False,
                            default=Defaults.STRING)
    member_brawler = db.Column('game_member_brawler', db.String(32), nullable=True,
                            default=Defaults.STRING)

    def __repr__(self):
        return f"Club League Game:\n" \
                f"|  id({self.game_id})\n" \
                f"|  season_id({self.season_id})\n" \
                f"|  game_day({self.game_day})\n" \
                f"|  game_mode({self.game_mode})\n" \
                f"|  game_map({self.game_map})\n" \
                f"|  game_result({self.game_result})\n" \
                f"|  game_trophies({self.game_trophies})\n" \
                f"|  member_tag({self.member_tag})\n" \
                f"|  member_name({self.member_name})\n" \
                f"|  member_brawler({self.member_brawler}))\n"
