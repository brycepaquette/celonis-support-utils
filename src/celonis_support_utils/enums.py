from enum import Enum


class DayOfWeek(Enum):
    """Enum for days of the week."""

    MO = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Region(Enum):
    """Enum for regions."""

    US = "us"
    EU = "eu"
    APAC = "apac"
    GLOBAL = "global"


class ServiceLevel(Enum):
    """Enum for service levels."""

    STANDARD = "Standard"
    PREMIUM = "Premium"
    PREMIER = "Premier"
    PREMIER_PLUS = "Premier Plus"
    MAXSUCCESS = "MaxSuccess"
