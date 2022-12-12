import urllib.parse

from club_league_tracker.models.db.club_member_details import ClubMemberDetails
from club_league_tracker.models.enums.defaults import Defaults
from club_league_tracker.networking.utils import RequestContents, RetryOptions, RequestType
from club_league_tracker.networking.utils import do_retryable_request

def get_club_member_details(member_tag:str, auth_token: str, proxies: dict) -> ClubMemberDetails:
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
