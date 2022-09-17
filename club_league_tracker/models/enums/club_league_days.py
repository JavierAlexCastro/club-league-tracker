from enum import Enum, unique
from locale import DAY_3

@unique
class CLUB_LEAGUE_DAYS(Enum):
    DAY_1 = "day 1"
    DAY_2 = "day 2"
    DAY_3 = "day 3"

    def describe(self):
         # self is the member here
         return self.name, self.value

    def __str__(self):
        return f"Club League Day: {self.value}"
