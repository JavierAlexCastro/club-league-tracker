import urllib.parse
import typing
import json

from club_league_tracker.models.bs_api.api_club_member import api_club_member, api_player_icon
from club_league_tracker.models.db.club_member import club_member
from club_league_tracker.models.enums.defaults import DEFAULTS
from club_league_tracker.models.enums.club_roles import CLUB_ROLES
from club_league_tracker.networking.utils import *

class APIClubMember:
    def __init__(self, icon, tag, name, trophies, role, name_color):
        self.icon = icon
        self.tag = tag
        self.name = name
        self.trophies = trophies
        self.role = role
        self.name_color = name_color

# uses db model
def get_club_members(club_tag:str, auth_token: str) -> typing.List[club_member]:
    encoded_club_tag = urllib.parse.quote(club_tag.encode('utf8'))
    request_url = f"https://api.brawlstars.com/v1/clubs/{encoded_club_tag}/members"
    request_headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    request_contents = RequestContents(url = request_url, headers = request_headers)
    request_retry_opts = RetryOptions(max_retries = 3, retry_buffer_seconds = 5)
    request_type = RequestType.GET

    res_tag = DEFAULTS.STRING
    res_name = DEFAULTS.STRING
    res_role = CLUB_ROLES.UNKNOWN
    res_trophies = DEFAULTS.INTEGER

    club_members = []
    try:
        raw_request_result = do_retryable_request(request_type = request_type, request_contents = request_contents, 
                                                retry_options = request_retry_opts)
        
        response_club_members = raw_request_result.json()['items']
        for member in response_club_members:
            if 'tag' in member:
                res_tag = str(member['tag'])
            if 'name' in member:
                res_name = str(member['name'])
            if 'role' in member:
                res_role = str(member['role'])
            if 'trophies' in member:
                res_trophies = member['trophies']
            
            club_members.append(club_member(tag = res_tag, name = res_name, role = res_role, trophies = res_trophies))
    except Exception as ex:
        # TODO: proper logging
        error_msg = f"Error getting club members for club {club_tag} - {str(ex)}"
        raise RuntimeError(error_msg)
    
    return club_members

# uses networking model
def get_api_club_members(club_tag: str, auth_token: str) -> typing.List[api_club_member]:
    encoded_club_tag = urllib.parse.quote(club_tag.encode('utf8'))
    request_url = f"https://api.brawlstars.com/v1/clubs/{encoded_club_tag}/members"
    request_headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    request_contents = RequestContents(url = request_url, headers = request_headers)
    request_retry_opts = RetryOptions(max_retries = 3, retry_buffer_seconds = 5)
    request_type = RequestType.GET

    res_tag = DEFAULTS.STRING
    res_name = DEFAULTS.STRING
    res_name_color = DEFAULTS.STRING
    res_role = CLUB_ROLES.UNKNOWN
    res_trophies = DEFAULTS.INTEGER
    res_icon_id = DEFAULTS.INTEGER

    api_club_members = []
    try:
        raw_request_result = do_retryable_request(request_type = request_type, request_contents = request_contents, 
                                                retry_options = request_retry_opts)
        
        response_club_members = raw_request_result.json()['items']
        for member in response_club_members:
            if 'tag' in member:
                res_tag = str(member['tag'])
            if 'name' in member:
                res_name = str(member['name'])
            if 'nameColor' in member:
                res_name_color = str(member['nameColor'])
            if 'role' in member:
                res_role = CLUB_ROLES(str(member['role']))
            if 'trophies' in member:
                res_trophies = member['trophies']
            if 'icon' in member and 'id' in member['icon']:
                res_icon_id = member['icon']['id']
            
            api_club_members.append(api_club_member(api_player_icon(res_icon_id), res_tag, res_name, 
                                                    res_trophies, res_role, res_name_color))
    except Exception as ex:
        # TODO: proper logging
        error_msg = f"Error getting club members for club {club_tag} - {str(ex)}"
        raise RuntimeError(error_msg)
    
    return api_club_members
