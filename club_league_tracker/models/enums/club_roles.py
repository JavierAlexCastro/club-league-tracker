from enum import Enum, unique

@unique
class ClubRoles(Enum):
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
    def is_leadership(cls, role: Enum) -> bool:
        return role in [ClubRoles.VICE_PRESIDENT, ClubRoles.PRESIDENT]

    @classmethod
    def is_member(cls, role: Enum) -> bool:
        return role in [ClubRoles.MEMBER, ClubRoles.SENIOR, ClubRoles.VICE_PRESIDENT,
                        ClubRoles.PRESIDENT]
