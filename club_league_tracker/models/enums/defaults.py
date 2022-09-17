from enum import Enum, unique

@unique
class DEFAULTS(Enum):
    STRING = "unknown"
    INTEGER = 0

    def describe(self):
         # self is the member here
         return self.name, self.value

    def __str__(self):
        return f"Default: {self.value}"
