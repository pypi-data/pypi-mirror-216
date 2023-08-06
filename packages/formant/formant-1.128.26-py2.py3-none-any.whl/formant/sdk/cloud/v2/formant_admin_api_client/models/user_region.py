from enum import Enum


class UserRegion(str, Enum):
    AMER = "AMER"
    EMEA = "EMEA"

    def __str__(self) -> str:
        return str(self.value)
