# from dataclasses import dataclass
import urllib.parse
import typing

from club_league_tracker.models.bs_api.api_club_member import ApiClubMember, ApiPlayerIcon
from club_league_tracker.models.db.club_member import ClubMember
from club_league_tracker.models.enums.defaults import Defaults
from club_league_tracker.models.enums.club_roles import ClubRoles
from club_league_tracker.networking.utils import RequestContents, RetryOptions, RequestType
from club_league_tracker.networking.utils import do_retryable_request

# @dataclass
# class APIClubMember:
#     def __init__(self, icon, tag, name, trophies, role, name_color):
#         self.icon = icon
#         self.tag = tag
#         self.name = name
#         self.trophies = trophies
#         self.role = role
#         self.name_color = name_color

# uses db model
def get_club_members(club_tag:str, auth_token: str, proxies: dict) -> typing.List[ClubMember]:
    encoded_club_tag = urllib.parse.quote(club_tag.encode('utf8'))
    request_retry_opts = RetryOptions(max_retries = 1, retry_buffer_seconds = 5)
    request_contents = RequestContents(
        url = f"https://api.brawlstars.com/v1/clubs/{encoded_club_tag}/members",
        headers = {
            "Authorization": f"Bearer {auth_token}"
        },
        timeout_seconds = 3,
        proxy = proxies
    )

    res_tag = Defaults.STRING
    res_name = Defaults.STRING
    res_role = ClubRoles.UNKNOWN
    res_trophies = Defaults.INTEGER

    club_members = []
    try:
        response_club_members = do_retryable_request(request_type = RequestType.GET,
                                                request_contents = request_contents,
                                                retry_options = request_retry_opts).json()['items']
        for member in response_club_members:
            if 'tag' in member:
                res_tag = str(member['tag'])
            if 'name' in member:
                res_name = str(member['name'])
            if 'role' in member:
                res_role = str(member['role'])
            if 'trophies' in member:
                res_trophies = member['trophies']

            club_members.append(
                ClubMember(tag = res_tag, club_tag = club_tag, name = res_name,
                            role = res_role, trophies = res_trophies))
    except Exception as ex:
        # TODO: proper logging
        raise RuntimeError(f"Error getting club members for club {club_tag}") from ex

    return club_members

# uses networking model
def get_api_club_members(club_tag: str, auth_token: str) -> typing.List[ApiClubMember]:
    encoded_club_tag = urllib.parse.quote(club_tag.encode('utf8'))
    request_retry_opts = RetryOptions(max_retries = 1, retry_buffer_seconds = 5)
    request_contents = RequestContents(
        url = f"https://api.brawlstars.com/v1/clubs/{encoded_club_tag}/members",
        headers = {
            "Authorization": f"Bearer {auth_token}"
        },
        timeout_seconds = 3)

    res_tag = Defaults.STRING
    res_name = Defaults.STRING
    res_name_color = Defaults.STRING
    res_role = ClubRoles.UNKNOWN
    res_trophies = Defaults.INTEGER
    res_icon_id = Defaults.INTEGER

    api_club_members = []
    try:
        response_club_members = do_retryable_request(request_type = RequestType.GET,
                                                request_contents = request_contents,
                                                retry_options = request_retry_opts).json()['items']
        for member in response_club_members:
            if 'tag' in member:
                res_tag = str(member['tag'])
            if 'name' in member:
                res_name = str(member['name'])
            if 'nameColor' in member:
                res_name_color = str(member['nameColor'])
            if 'role' in member:
                res_role = ClubRoles(str(member['role']))
            if 'trophies' in member:
                res_trophies = member['trophies']
            if 'icon' in member and 'id' in member['icon']:
                res_icon_id = member['icon']['id']

            api_club_members.append(ApiClubMember(ApiPlayerIcon(res_icon_id), res_tag, res_name,
                                                    res_trophies, res_role, res_name_color))
    except Exception as ex:
        # TODO: proper logging
        raise RuntimeError(f"Error getting club members for club {club_tag}") from ex

    return api_club_members
