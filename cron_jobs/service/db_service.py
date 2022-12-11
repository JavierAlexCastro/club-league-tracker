import typing

from cron_jobs.db import db_session
from club_league_tracker.models.db import ClubMember
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

# TODO: remove side effect of updating no_longer_members into its own function
def upsert_club_members(club_members: typing.List[ClubMember]):
    if len(club_members) < 1: return

    updates = 0
    insertions = 0
    deletions = 0

    db_members = None
    try:
        db_members = get_club_members(club_members[0].club_tag)
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex

    db_members_tags = (member.tag for member in db_members)
    req_members_tags = (member.tag for member in club_members)

    no_longer_members = [i for i in db_members if not i.club_tag in req_members_tags]
    new_members = [i for i in club_members if not i.club_tag in db_members_tags]
    # continuing_members = [i for i in club_members if i.club_tag in db_members_tags]
    continuing_members = [i for i in db_members if i.club_tag in req_members_tags]

    try:
        for member in new_members:
            db_session.add(member)
            insertions+=1

        for member in continuing_members:
            member.update(db_session, member.tag, member.club_tag, member.name, member.role, member.trophies)
            updates+=1

        for member in no_longer_members:
            member.soft_remove_from_club(db_session, member.tag, member.club_tag, member.name, ClubRoles.NOT_MEMBER.value, member.trophies)
            deletions+=1
        db_session.commit()
         # TODO: proper logging
        print(f"Successfully commited members to DB")
        print(f"commited: {len(new_members)} additions")
        print(f"commited: {len(continuing_members)} updates")
        print(f"commited: {len(no_longer_members)} de-activations")
    except Exception as ex:
        raise RuntimeError(f"Failed to commit club_members to DB. Insertions {insertions}, Updates {updates}, Deletions {deletions}") from ex

#TODO: this method should not sort. Instead a sort__service should exist with sorting methods as needed
def get_club_members(club_tag: str) -> typing.List[ClubMember]:
    members = None
    try:
        members = ClubMember.query \
                .filter(ClubMember.club_tag.endswith(club_tag)) \
                .order_by(ClubMember.trophies.desc()) \
                .all()
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex
    
    return members
