from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubLeagueGame(Base):
    __tablename__ = 'club_league_games'
    game_id = Column('game_id', Integer, nullable=False, autoincrement=True, primary_key=True)
    season_id = Column('season_id', Integer, ForeignKey('club_league_season.season_id'), nullable=True)
    game_season_day = Column('game_season_day', String(16), nullable=True, default=Defaults.STRING.value)
    game_date = Column('game_date', String(24), nullable=False, default=Defaults.STRING.value)
    game_mode = Column('game_mode', String(64), nullable=False, default=Defaults.STRING.value)
    game_map = Column('game_map', String(64), nullable=False, default=Defaults.STRING.value)
    game_result = Column('game_result', String(16), nullable=False, default=Defaults.STRING.value)
    game_trophies = Column('game_trophies', Integer, nullable=False, default=Defaults.INTEGER.value)
    member_tag = Column('member_tag', String(16), ForeignKey('club_member.member_tag'), nullable=False)
    member_name = Column('game_member_name', String(32), nullable=False, default=Defaults.STRING.value)
    
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
