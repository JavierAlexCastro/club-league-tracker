import urllib.parse
import typing

from club_league_tracker.models.db.club_member_details import ClubMemberDetails
from club_league_tracker.models.db.club_league_game import ClubLeagueGame
from club_league_tracker.models.enums.defaults import Defaults
from club_league_tracker.networking.utils import RequestContents, RetryOptions, RequestType
from club_league_tracker.networking.utils import do_retryable_request
from club_league_tracker.service.db_service import is_cl_game_already_stored

cl_excluded_game_mode = ["soloShowdown", "duoShowdown"]
cl_game_type = ["teamRanked", "ranked"]
cl_trophy_change = [3, 5, 7, 9]

def get_club_member_details(member_tag: str, auth_token: str, proxies: dict) -> ClubMemberDetails:
    encoded_member_tag = urllib.parse.quote(member_tag.encode('utf8'))
    request_retry_opts = RetryOptions(max_retries = 1, retry_buffer_seconds = 5)
    request_contents = RequestContents(
        url = f"https://api.brawlstars.com/v1/players/{encoded_member_tag}",
        headers = {
            "Authorization": f"Bearer {auth_token}"
        },
        timeout_seconds = 3,
        proxy = proxies
    )

    res_start_date = None
    res_departure_date = None
    res_victories_trios = Defaults.INTEGER.value
    res_victories_duos = Defaults.INTEGER.value
    res_victories_solo = Defaults.INTEGER.value

    member_details = None
    try:
        response_club_member = do_retryable_request(request_type = RequestType.GET,
                                                request_contents = request_contents,
                                                retry_options = request_retry_opts).json()
        if 'tag' in response_club_member:
            res_tag = str(response_club_member['tag'])
        if '3vs3Victories' in response_club_member:
            res_victories_trios = response_club_member['3vs3Victories']
        if 'duoVictories' in response_club_member:
            res_victories_duos = response_club_member['duoVictories']
        if 'soloVictories' in response_club_member:
            res_victories_solo = response_club_member['soloVictories']

        member_details = ClubMemberDetails(member_tag = res_tag, start_date = res_start_date, departure_date = res_departure_date,
                        victories_trios = res_victories_trios, victories_duos = res_victories_duos, victories_solo = res_victories_solo)
    except Exception as ex:
        # TODO: proper logging
        raise RuntimeError(f"Error getting club member details for member {member_tag}") from ex

    return member_details

def get_club_member_cl_games(member_tag: str, member_name: str, season_id: int, auth_token: str, proxies: dict) -> typing.List[ClubLeagueGame]:
    encoded_member_tag = urllib.parse.quote(member_tag.encode('utf8'))
    request_retry_opts = RetryOptions(max_retries = 1, retry_buffer_seconds = 5)
    request_contents = RequestContents(
        url = f"https://api.brawlstars.com/v1/players/{encoded_member_tag}/battlelog",
        headers = {
            "Authorization": f"Bearer {auth_token}"
        },
        timeout_seconds = 3,
        proxy = proxies
    )

    res_type = Defaults.STRING.value
    res_game_date = Defaults.STRING.value
    res_game_mode = Defaults.STRING.value
    res_game_map = Defaults.STRING.value
    res_game_result = Defaults.STRING.value
    res_game_trophies = Defaults.INTEGER.value

    club_league_games = []
    try:
        response_club_member_games = do_retryable_request(request_type = RequestType.GET,
                                                request_contents = request_contents,
                                                retry_options = request_retry_opts).json()["items"]
        for game in response_club_member_games:
            if 'battleTime' in game:
                res_game_date = str(game['battleTime'])
            if 'event' in game:
                res_event = game['event']
                if 'mode' in res_event:
                    res_game_mode = str(res_event['mode'])
                if 'map' in res_event:
                    res_game_map = str(res_event['map'])
            if 'battle' in game:
                res_battle = game['battle']
                if 'type' in res_battle:
                    res_type = str(res_battle['type'])
                if 'result' in res_battle:
                    res_game_result = str(res_battle['result'])
                if 'trophyChange' in res_battle:
                    res_game_trophies = res_battle['trophyChange']

            # now_time = datetime.now()
            # game_time = datetime.strptime(res_game_date, "%Y%m%dT%H%M%S.%fZ")
            is_duplicate = is_cl_game_already_stored(res_game_date)
            # This determines if it is a club league game compared to just a regular game
            if res_type in cl_game_type and res_game_trophies in cl_trophy_change and res_game_mode not in cl_excluded_game_mode and not is_duplicate:
                club_league_games.append(ClubLeagueGame(season_id = season_id, game_season_day = None, game_date = res_game_date,
                            game_mode = res_game_mode, game_map = res_game_map, game_result = res_game_result,
                            game_trophies = res_game_trophies, member_tag = member_tag, member_name = member_name))
    except Exception as ex:
        # TODO: proper logging
        raise RuntimeError(f"Error getting battle log for member {member_tag}") from ex

    return club_league_games
