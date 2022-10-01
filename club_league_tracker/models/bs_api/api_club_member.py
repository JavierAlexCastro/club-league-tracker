from dataclasses import dataclass
from club_league_tracker.models.bs_api.api_player_icon import ApiPlayerIcon
from club_league_tracker.models.enums.club_roles import ClubRoles

@dataclass
class ApiClubMember:
    player_icon: ApiPlayerIcon
    tag: str
    name: str
    trophies: int
    role: ClubRoles
    name_color: str
