import os
import typing

from club_league_tracker.models.db.club_league_game import ClubLeagueGame

from cron_jobs.service import db_service
from cron_jobs.service import api_service

if __name__ == "__main__":
    auth_token = os.environ.get('BS_API_KEY')
    club_tag = "#292QGGUUJ" # IX Electron

    season = db_service.fetch_current_cl_season()
    members = db_service.get_club_members(club_tag)

    if members is not None:
        for member in members:
            cl_games = api_service.get_club_league_games(member.tag, member.name, season.id, auth_token) # TODO: list vs List
            db_service.add_club_league_games(cl_games)
