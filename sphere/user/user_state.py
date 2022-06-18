import enum


class UserState(enum.Enum):
    ACTIVE = "ACTIVE"
    DE_ACTIVATED = "DE_ACTIVATED"
    DELETED = "DELETED"
