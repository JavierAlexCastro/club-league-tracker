from enum import Enum, unique

@unique
class CLUB_ROLES(Enum):
    MEMBER = "member"
    SENIOR = "senior"
    VICE_PRESIDENT = "vice president"
    PRESIDENT = "president"

    def describe(self):
         # self is the member here
         return self.name, self.value

    def __str__(self):
        return f"Role: {self.value}"

    @classmethod
    def is_leadership(role: CLUB_ROLES) -> bool:
        return role in [CLUB_ROLES.VICE_PRESIDENT, CLUB_ROLES.PRESIDENT]
