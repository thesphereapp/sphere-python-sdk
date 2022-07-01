import enum


class UserState(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DE_ACTIVATED = "DE_ACTIVATED"
    DELETED = "DELETED"
