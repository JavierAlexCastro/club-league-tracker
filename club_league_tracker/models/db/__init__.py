from club_league_tracker.models.db.club_member import *
from club_league_tracker.models.db.club_member_details import *
from club_league_tracker.models.db.club_league_season import *
from club_league_tracker.models.db.club_league_game import *

from club_league_tracker.models.enums.club_league_days import *
from club_league_tracker.models.enums.club_roles import *
from club_league_tracker.models.enums.defaults import *

# keep adding db model classes to allow for:
#
# from club_league_tracker.models.db import *
# club_member.query.all()
