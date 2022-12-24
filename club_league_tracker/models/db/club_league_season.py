from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubLeagueSeason(Base):
    __tablename__ = 'club_league_season'
    id = Column('season_id', Integer, nullable=False, primary_key=True)
    week = Column('season_week', String(16), nullable=True, default=Defaults.STRING)
    start_members = Column('season_start_members', Integer, nullable=True,
                                default=Defaults.INTEGER)
    end_members = Column('season_end_members', Integer, nullable=True,
                                default=Defaults.INTEGER)
    day_one_trophies = Column('season_day_one_trophies', Integer, nullable=True,
                                default=Defaults.INTEGER)
    day_two_trophies = Column('season_day_two_trophies', Integer, nullable=True,
                                default=Defaults.INTEGER)
    day_three_trophies = Column('season_day_three_trophies', Integer, nullable=True,
                                default=Defaults.INTEGER)
    total_trophies = Column('season_total_trophies', Integer, nullable=True,
                                default=Defaults.INTEGER)
    participation = Column('season_participation', Integer, nullable=True,
                                default=Defaults.INTEGER)
    is_current = Column('season_is_current', Boolean, nullable=False)
    club_league_games = relationship('ClubLeagueGame',
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
