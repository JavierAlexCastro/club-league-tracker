from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubMember(Base):
    tag = Column('member_tag', String(16), primary_key=True)
    club_tag = Column('club_tag', String(16), nullable=False, default=Defaults.STRING)
    name = Column('member_name', String(32), nullable=False, default=Defaults.STRING)
    role = Column('member_role', String(32), nullable=False, default=Defaults.STRING)
    trophies = Column('member_trophies', Integer, nullable=False, default=Defaults.INTEGER)
    club_league_games = relationship('ClubLeagueGames', backref='club_member', lazy=True)

    def __repr__(self):
        return f"Club Member:\n" \
                f"|  tag({self.tag})\n" \
                f"|  clug_tag({self.club_tag})\n" \
                f"|  name({self.name})\n" \
                f"|  role({self.role})\n" \
                f"|  trophies({self.trophies}))\n"
