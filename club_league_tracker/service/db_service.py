import typing

from club_league_tracker.db import db_session
from club_league_tracker.models.db import ClubMember
from club_league_tracker.models.db import ClubMemberDetails
from club_league_tracker.models.db import ClubLeagueSeason
from club_league_tracker.models.db import ClubLeagueGame
from club_league_tracker.models.enums.club_roles import ClubRoles

def save_club_members(club_members: typing.List[ClubMember]):
    try:
        for member in club_members:
            db_session.add(member)
        db_session.commit()
        # TODO: proper logging
        print(f"Successfully commited {len(club_members)} records to DB")
    except Exception as ex:
        raise RuntimeError("Failed to commit club_members to DB") from ex

#TODO: this method should not sort. Instead a sort__service should exist with sorting methods as needed
def get_club_members(club_tag: str) -> typing.List[ClubMember]:
    members = None
    try:
        members = ClubMember.query \
                .filter(ClubMember.club_tag.endswith(club_tag)) \
                .filter(ClubMember.role.is_distinct_from(ClubRoles.NOT_MEMBER.value)) \
                .order_by(ClubMember.trophies.desc()) \
                .all()
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex
    
    return members

def get_club_member(member_tag: str) -> ClubMember:
    member = None
    print(f"Fetching club member {member_tag} from DB")
    try:
        member = ClubMember.query.get(member_tag)
        print(f"Got club member {member_tag} from DB")
    except Exception as ex:
        raise RuntimeError(f"Failed to get club_member {member_tag} from DB") from ex
    
    return member

def get_club_member_details(member_tag: str) -> ClubMemberDetails:
    member_details = None
    print(f"Fetching club member details from DB for {member_tag}")
    try:
        member_details = ClubMemberDetails.query.get(member_tag)
        print(f"Got club member details from DB for {member_tag}")
    except Exception as ex:
        raise RuntimeError(f"Failed to get club_member_details for member {member_tag} from DB") from ex
    
    return member_details

def get_club_league_season(season_id: str) -> ClubLeagueSeason:
    cl_season = None
    print(f"Fetching club league season with id {season_id} from DB")
    try:
        cl_season = ClubLeagueSeason.query.get(season_id)
        print(f"Got club league season from DB for {season_id}")
    except Exception as ex:
        raise RuntimeError(f"Failed to get club_league_season with id {season_id} from DB") from ex
    return cl_season

def get_latest_club_league_season() -> ClubLeagueSeason:
    cl_season = None
    print("Fetching latest club league season from DB")
    try:
        cl_season = ClubLeagueSeason.query \
            .filter(ClubLeagueSeason.is_current.is_(True))
        if cl_season is None:
            raise RuntimeError("Could not find latest club_leage_season")
        print(f"Got latest club league season from DB")
    except Exception as ex:
        raise RuntimeError(f"Failed to get latest club_league_season from DB") from ex
    return cl_season

def is_cl_game_already_stored(timestamp: str) -> bool:
    is_duplicate = False
    stored_game = db_session.query(ClubLeagueGame) \
        .filter(ClubLeagueGame.game_date == timestamp) \
        .first()
    if stored_game is not None:
        print(f"Warning! Club league game with timestamp {timestamp} is already stored")
        is_duplicate = True

    return is_duplicate

def get_club_league_games_for_season(season_id: int, member_tag: str) -> typing.List[ClubLeagueGame]:
    games = []
    print(f"Fetching club league season {season_id} games for member {member_tag} from DB")
    try:
        games = db_session.query(ClubLeagueGame) \
            .filter(ClubLeagueGame.season_id == season_id, ClubLeagueGame.member_tag == member_tag) \
            .all()
        if games is None or len(games) == 0:
            raise RuntimeError(f"Could not find club league season {season_id} games for member {member_tag}")
        print(f"Got club league games for season {season_id} and member {member_tag} from DB")
    except Exception as ex:
        raise RuntimeError(f"Failed to get club league season {season_id} games for member {member_tag} from DB") from ex
    return games
