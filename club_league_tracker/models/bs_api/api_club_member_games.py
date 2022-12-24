from dataclasses import dataclass
import typing

from club_league_tracker.models.bs_api.api_player_icon import ApiPlayerIcon
from club_league_tracker.models.enums.club_roles import ClubRoles

@dataclass
class ClubMemberGameEvent:
    id: int
    map: str

@dataclass
class ClubMemberGameStarPlayerBrawler:
    id: int
    name: str
    power: int
    trophies: int

@dataclass
class ClubMemberGamePlayer:
    tag: str
    name: str
    brawler: ClubMemberGameStarPlayerBrawler

@dataclass
class ClubMemberGameBattle:
    mode: str
    type: str
    result: str
    duration: int
    star_player: ClubMemberGamePlayer
    teams: typing.List[ClubMemberGamePlayer]

@dataclass
class ClubMemberGame:
    battle_time: str
    event: ClubMemberGameEvent
    battle: ClubMemberGameBattle
