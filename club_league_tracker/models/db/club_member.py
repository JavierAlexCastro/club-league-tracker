from club_league_tracker.db import db
from club_league_tracker.models.enums.defaults import Defaults

class ClubMember(db.Model):
    tag = db.Column('member_tag', db.String(16), primary_key=True)
    club_tag = db.Column('club_tag', db.String(16), nullable=False, default=Defaults.STRING)
    name = db.Column('member_name', db.String(32), nullable=False, default=Defaults.STRING)
    role = db.Column('member_role', db.String(32), nullable=False, default=Defaults.STRING)
    trophies = db.Column('member_trophies', db.Integer, nullable=False, default=Defaults.INTEGER)
    club_league_games = db.relationship('ClubLeagueGames', backref='club_member', lazy=True)

    def __repr__(self):
        return f"Club Member:\n" \
                f"|  tag({self.tag})\n" \
                f"|  clug_tag({self.club_tag})\n" \
                f"|  name({self.name})\n" \
                f"|  role({self.role})\n" \
                f"|  trophies({self.trophies}))\n"
