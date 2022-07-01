import enum


class ExternalReference(str, enum.Enum):
    STRIPE_CHARGE_ID = "STRIPE_CHARGE_ID"
