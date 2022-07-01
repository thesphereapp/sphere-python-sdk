import enum


class LocationState(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DE_ACTIVATED = "DE_ACTIVATED"
    DELETED = "DELETED"
