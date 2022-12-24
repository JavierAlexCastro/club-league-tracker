import typing

from club_league_tracker.models.db.club_member import ClubMember
from club_league_tracker.models.db.club_member_details import ClubMemberDetails
from club_league_tracker.models.db.club_league_game import ClubLeagueGame
from club_league_tracker.networking.bs_clubs import get_club_members
from club_league_tracker.networking.bs_players import get_club_member_details, get_club_member_cl_games


def get_club_league_games(member_tag: str, member_name: str, season_id: int, token: str) -> typing.List[ClubLeagueGame]:
    cl_games = None
    try:
        cl_games = get_club_member_cl_games(member_tag = member_tag, 
                                            member_name = member_name, 
                                            season_id = season_id, 
                                            auth_token = token,
                                            proxies = None)
        print(f"Got {len(cl_games)} club league games for member {member_tag}")
    except Exception as ex:
        raise RuntimeError(f"Error getting club member {member_tag} club league games from API")
    
    return cl_games

def get_members_from_api(club_tag: str, token: str) -> typing.List[ClubMember]:
    members = None
    try:
        members = get_club_members(club_tag=club_tag,
                                    auth_token=token,
                                    proxies=None)
        print("Got club members from API")
    except Exception as ex:
        raise RuntimeError("Error getting club members from API") from ex

    return members

def get_member_details_from_api(member_tag: str, token: str) -> ClubMemberDetails:
    member_details = None
    try:
        member_details = get_club_member_details(member_tag=member_tag,
                                                auth_token=token,
                                                proxies=None)
        print(f"Got club member details from API for {member_tag}")
    except Exception as ex:
        raise RuntimeError(f"Error gettting club member details from API for member {member_tag}")
    
    return member_details

def get_member_count(club_tag: str, token: str) -> int:
    members = get_members_from_api(club_tag, token)
    return len(members)
