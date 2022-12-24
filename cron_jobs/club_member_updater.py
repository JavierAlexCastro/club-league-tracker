import os
import typing

from club_league_tracker.models.db.club_member import ClubMember
from club_league_tracker.networking.bs_clubs import get_club_members

from cron_jobs.service import db_service
from cron_jobs.service import api_service

# TODO: proper logging
def handle_club_members(members: typing.List[ClubMember], token: str) -> None:
    try:    
        db_service.upsert_club_members(members, token)
        print("Saved club members to DB")
    except Exception as ex:
        raise RuntimeError("Error saving club members to DB") from ex

if __name__ == "__main__":
    auth_token = os.environ.get('BS_API_KEY')
    club_tag = "#292QGGUUJ" # IX Electron

    club_members = api_service.get_members_from_api(club_tag, auth_token)
    handle_club_members(club_members, auth_token)
