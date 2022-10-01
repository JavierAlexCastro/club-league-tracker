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
