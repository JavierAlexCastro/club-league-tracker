from club_league_tracker.db import db
from club_league_tracker.models.enums.defaults import Defaults

class ClubLeagueSeason(db.Model):
    id = db.Column('season_id', db.Integer, nullable=False, primary_key=True)
    week = db.Column('season_week', db.String(16), nullable=False, default='unknown')
    start_members = db.Column('season_start_members', db.Integer, nullable=True,
                                default=Defaults.INTEGER)
    end_members = db.Column('season_end_members', db.Integer, nullable=True,
                                default=Defaults.INTEGER)
    day_one_trophies = db.Column('season_day_one_trophies', db.Integer, nullable=False,
                                default=Defaults.INTEGER)
    day_two_trophies = db.Column('season_day_two_trophies', db.Integer, nullable=False,
                                default=Defaults.INTEGER)
    day_three_trophies = db.Column('season_day_three_trophies', db.Integer, nullable=False,
                                default=Defaults.INTEGER)
    total_trophies = db.Column('season_total_trophies', db.Integer, nullable=False,
                                default=Defaults.INTEGER)
    participation = db.Column('season_participation', db.Integer, nullable=True,
                                default=Defaults.INTEGER)
    is_current = db.Column('season_is_current', db.Boolean, nullable=False)
    club_league_games = db.relationship('club_league_games',
                                        backref='club_league_season', lazy=True)

    def __repr__(self):
        return f"Club League Season:\n" \
                f"|  id({self.id})\n" \
                f"|  week({self.week})\n" \
                f"|  start_members({self.start_members})\n" \
                f"|  end_members({self.end_members})\n" \
                f"|  day_one_trophies({self.day_one_trophies})\n" \
                f"|  day_two_trophies({self.day_two_trophies})\n" \
                f"|  day_three_trophies({self.day_three_trophies})\n" \
                f"|  total_trophies({self.total_trophies})\n" \
                f"|  participation({self.participation})\n" \
                f"|  is_current({self.is_current}))\n"
