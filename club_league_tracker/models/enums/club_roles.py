from enum import Enum, unique

@unique
class CLUB_ROLES(Enum):
    MEMBER = "member"
    SENIOR = "senior"
    VICE_PRESIDENT = "vicePresident"
    PRESIDENT = "president"
    UNKNOWN = "unknown"
    NOT_MEMBER = "notMember"

    def describe(self):
         # self is the member here
         return self.name, self.value

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def is_leadership(role: Enum) -> bool:
        return role in [CLUB_ROLES.VICE_PRESIDENT, CLUB_ROLES.PRESIDENT]
    
    @classmethod
    def is_member(role: Enum) -> bool:
        return role in [CLUB_ROLES.MEMBER, CLUB_ROLES.SENIOR, CLUB_ROLES.VICE_PRESIDENT, CLUB_ROLES.PRESIDENT]
