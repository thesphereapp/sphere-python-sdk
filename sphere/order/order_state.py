import enum


class OrderState(enum.Enum):
    NEW = "NEW"
    PAYMENT_IN_PROGRESS = "PAYMENT_IN_PROGRESS"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
