import os

from datetime import datetime
from club_league_tracker.models.db.club_league_season import ClubLeagueSeason
from cron_jobs.service import api_service
from cron_jobs.service import db_service

def deprecate_previous_season() -> None:
    current_season = db_service.fetch_current_cl_season()
    if current_season is not None:
        print(f"Deprecating season {current_season.week}")
        current_season.is_current = False
        db_service.save_club_league_season(current_season)
        print(f"Deprecated season {current_season.week}")
    else:
        print("Warning: Found no previous club league season to deprecate")

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
        week = season_week,
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
    print(f"Created club league season {new_season.week}")
    deprecate_previous_season()
    db_service.save_club_league_season(new_season)
    print(f"Saved season active club league season {new_season.week} to DB")