import enum


class AccountType(str, enum.Enum):
    SAVINGS = "SAVINGS"
    CHECKING = "CHECKING"
