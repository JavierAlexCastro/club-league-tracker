import os
import typing

from club_league_tracker.models.db.club_member import ClubMember
from club_league_tracker.networking.bs_clubs import get_club_members

from cron_jobs.service.db_service import upsert_club_members
from cron_jobs.service import db_service

# TODO: proper logging
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

# TODO: proper logging
def handle_club_members(members: typing.List[ClubMember]) -> None:
    try:    
        db_service.upsert_club_members(members)
        print("Saved club members to DB")
    except Exception as ex:
        raise RuntimeError("Error saving club members to DB") from ex

if __name__ == "__main__":
    auth_token = os.environ.get('BS_API_KEY')
    club_tag = "#292QGGUUJ" # IX Electron

    club_members = get_members_from_api(club_tag, auth_token)
    handle_club_members(club_members)
