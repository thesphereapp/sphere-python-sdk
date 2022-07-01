import enum


class MeasurementUnit(str, enum.Enum):
    KILOGRAM = "KILOGRAM"
    METER = "METER"
    AMOUNT = "AMOUNT"
