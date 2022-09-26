import typing

from club_league_tracker.db import db
from club_league_tracker.models.db import *

def save_club_members(club_members: typing.List[club_member]):
    try:
        for member in club_members:
            db.session.add(member)
        db.session.commit()
        # TODO: proper logging
        print(f"Successfully commited {len(club_members)} records to DB")
    except Exception as ex:
        error_msg = "Failed to commit club_members to DB"
        raise RuntimeError(f"{error_msg} - {str(ex)}")
