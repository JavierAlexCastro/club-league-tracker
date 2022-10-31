import typing

from club_league_tracker.db import db
from club_league_tracker.models.db import ClubMember

def save_club_members(club_members: typing.List[ClubMember]):
    try:
        for member in club_members:
            db.session.add(member)
        db.session.commit()
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
                .order_by(ClubMember.trophies.desc()) \
                .all()
    except Exception as ex:
        raise RuntimeError("Failed to get club_members from DB") from ex
    
    return members
