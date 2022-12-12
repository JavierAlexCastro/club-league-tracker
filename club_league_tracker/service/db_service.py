import typing

from club_league_tracker.db import db_session
from club_league_tracker.models.db import ClubMember
from club_league_tracker.models.db import ClubMemberDetails
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
    try:
        member = ClubMember.query.get(member_tag)
    except Exception as ex:
        raise RuntimeError(f"Failed to get club_member {member_tag} from DB") from ex
    
    return member

def get_club_member_details(member_tag: str) -> ClubMemberDetails:
    member_details = None
    try:
        member_details = ClubMemberDetails.query.get(member_tag)
    except Exception as ex:
        raise RuntimeError(f"Failed to get club_member_details for member {member_tag} from DB") from ex
    
    return member_details
