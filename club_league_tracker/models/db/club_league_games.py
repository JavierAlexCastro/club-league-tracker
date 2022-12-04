from sqlalchemy import Column, Integer, String, ForeignKey
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubLeagueGames(Base):
    game_id = Column('game_id', Integer,nullable=False, primary_key=True)
    season_id = Column(Integer, ForeignKey('club_league_season.season_id'), nullable=False)
    game_day = Column('game_day', String(16), nullable=False, default=Defaults.STRING)
    game_mode = Column('game_mode', String(64), nullable=False, default=Defaults.STRING)
    game_map = Column('game_map', String(64), nullable=False, default=Defaults.STRING)
    game_result = Column('game_result', String(16), nullable=False, default=Defaults.STRING)
    game_trophies = Column('game_trophies', Integer, nullable=False, default=Defaults.INTEGER)
    member_tag = Column(String(16), ForeignKey('club_member.member_tag'), nullable=False)
    member_name = Column('game_member_name', String(32), nullable=False,
                            default=Defaults.STRING)
    member_brawler = Column('game_member_brawler', String(32), nullable=True,
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
