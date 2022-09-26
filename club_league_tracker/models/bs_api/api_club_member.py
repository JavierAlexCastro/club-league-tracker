from club_league_tracker.models.bs_api.api_player_icon import api_player_icon
from club_league_tracker.models.enums.club_roles import CLUB_ROLES

class api_club_member:
    def __init__(self, api_player_icon: api_player_icon, tag: str, name: str,
                trophies: int, role: CLUB_ROLES, name_color: str):
        self.api_player_icon = api_player_icon
        self.tag = tag
        self.name = name
        self.trophies = trophies
        self.role = role
        self.name_color = name_color