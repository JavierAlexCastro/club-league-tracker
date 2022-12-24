import os

from datetime import datetime
from club_league_tracker.models.db.club_league_season import ClubLeagueSeason
from cron_jobs.service import api_service
from cron_jobs.service import db_service

def deprecate_previous_season() -> None:
    current_season = db_service.fetch_current_cl_season()
    current_season.is_current = False
    db_service.save_club_league_season(current_season)

def create_season(club_tag: str, token: str) -> ClubLeagueSeason:
    today = datetime.now().isocalendar()
    season_week = f"s{today.week}-{today.year}"

    member_count = api_service.get_member_count(club_tag=club_tag, token=auth_token)

    # These will get populated as times goes by, for now we set them to None
    end_members = None
    one_trophies = None
    two_trophies = None
    three_trophies = None
    total_trophies = None
    participation = None

    return ClubLeagueSeason(
        season_week = season_week,
        start_members = member_count,
        end_members = end_members,
        day_one_trophies = one_trophies,
        day_two_trophies = two_trophies,
        day_three_trophies = three_trophies,
        total_trophies = total_trophies,
        participation = participation,
        is_current = True
    )

if __name__ == "__main__":
    auth_token = os.environ.get('BS_API_KEY')
    club_tag = "#292QGGUUJ" # IX Electron
    new_season = create_season(club_tag, auth_token)
    deprecate_previous_season()
    db_service.save_club_league_season(new_season)