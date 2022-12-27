import typing

from cron_jobs.db import db_session
from cron_jobs.service import api_service

from sqlalchemy.sql import func

from club_league_tracker.models.db import ClubMember, ClubLeagueSeason, ClubLeagueGame, ClubRoles
from club_league_tracker.service.db_service import get_club_member_details as db_get_club_member_details

# TODO: factor whole class, especially separate responsibilities and reduce tight coupling

def fetch_current_cl_season() -> ClubLeagueSeason:
    current_season = None
    try:
        print("Fetching current club league season")
        current_season = db_session.query(ClubLeagueSeason) \
            .filter(ClubLeagueSeason.is_current.is_(True)) \
            .first()
    except Exception as ex:
        raise RuntimeError("Failed to fetch current club league season from DB") from ex
    
    return current_season

def save_club_league_season(season: ClubLeagueSeason):
    try:
        db_session.add(season)
        db_session.commit()
        print(f"Successfully added club league season {season.week} to DB")
    except Exception as ex:
        raise RuntimeError(f"Failed to commit club_league_season {season.week} to DB") from ex

def deprecate_club_league_season(season: ClubLeagueSeason):
    try:
        print(f"Deprecating season {season.week}")
        setattr(season, 'season_is_current', False)
        # db_session.add(season)
        db_session.commit()
        print(f"Deprecated season {season.week}")
    except Exception as ex:
        raise RuntimeError(f"Failed to update club league season {season.week} on DB") from ex

def save_club_members(club_members: typing.List[ClubMember]):
    try:
        for member in club_members:
            db_session.add(member)
        db_session.commit()
        # TODO: proper logging
        print(f"Successfully commited {len(club_members)} records to DB")
    except Exception as ex:
        raise RuntimeError("Failed to commit club_members to DB") from ex

# TODO: remove side effect of updating no_longer_members into its own function
# TODO: refactor so db_service only does db operations and not other logic
def upsert_club_members(club_members: typing.List[ClubMember], auth_token: str):
    if len(club_members) < 1: return

    updates = 0
    insertions = 0
    deletions = 0

    db_members = None
    try:
        db_members = get_all_club_members(club_members[0].club_tag)
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex

    db_members_tags = [member.tag for member in db_members]
    req_members_tags = [member.tag for member in club_members]

    no_longer_members = [i for i in db_members if i.tag not in req_members_tags]
    new_members = [i for i in club_members if i.tag not in db_members_tags]
    continuing_members = [i for i in club_members if i.tag in db_members_tags]
    # continuing_members = [i for i in db_members if i.tag in req_members_tags]

    print(f"db member tags: {len(db_members_tags)}")
    print(f"req member tags: {len(req_members_tags)}")

    print(f"No longer members: {len(no_longer_members)}")
    print(f"New members: {len(new_members)}")
    print(f"Continuing members: {len(continuing_members)}")

    try:
        for member in new_members:
            db_session.add(member)

            member_details = api_service.get_member_details_from_api(member.tag, auth_token)
            member_details.start_date = func.now()
            db_session.add(member_details)

            insertions+=1

        for member in continuing_members:
            member.update(db_session, member.tag, member.club_tag, member.name, member.role, member.trophies)

            member_details = api_service.get_member_details_from_api(member.tag, auth_token)
            db_member_details = db_get_club_member_details(member.tag)
            if db_member_details is None: # probably because was added before member_details were a thing
                db_session.add(member_details)
            else:
                member_details.update(db_session, member.tag, db_member_details.start_date, None, member_details.victories_trios, 
                                    member_details.victories_duos, member_details.victories_solo)
            updates+=1

        for member in no_longer_members:
            member.update(db_session, member.tag, member.club_tag, member.name, ClubRoles.NOT_MEMBER.value, member.trophies)

            member_details = api_service.get_member_details_from_api(member.tag, auth_token)
            db_member_details = db_get_club_member_details(member.tag)
            if db_member_details is None: # probably because was added before member_details were a thing
                db_session.add(member_details)
            else:
                member_details.update(db_session, member.tag, db_member_details.start_date, func.now(), member_details.victories_trios, 
                                        member_details.victories_duos, member_details.victories_solo)
            deletions+=1
        db_session.commit()
         # TODO: proper logging
        print(f"Successfully commited members to DB")
        print(f"commited: {len(new_members)} additions")
        print(f"commited: {len(continuing_members)} updates")
        print(f"commited: {len(no_longer_members)} de-activations")
    except Exception as ex:
        raise RuntimeError(f"Failed to commit club_members to DB. Insertions {insertions}, Updates {updates}, Deletions {deletions}") from ex

def add_club_league_games(cl_games: typing.List[ClubLeagueGame]):
    try:
        for game in cl_games:
            db_session.add(game)
        db_session.commit()
    except Exception as ex:
        raise RuntimeError(f"Failed to add {len(cl_games)} club league games for {cl_games[0].member_tag} to DB.") from ex


def get_club_members(club_tag: str) -> typing.List[ClubMember]:
    members = None
    try:
        members = ClubMember.query \
                .filter(ClubMember.club_tag.endswith(club_tag)) \
                .filter(ClubMember.role.is_distinct_from(ClubRoles.NOT_MEMBER.value)) \
                .all()
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex
    
    return members

def get_all_club_members(club_tag: str) -> typing.List[ClubMember]:
    members = None
    try:
        members = ClubMember.query \
                .filter(ClubMember.club_tag.endswith(club_tag)) \
                .all()
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex
    
    return members
