from enum import Enum, auto


class DayOfWeek(Enum):
    """Enum for days of the week.
    Note: abbreviated names (MO, TUE, WED) are legacy — do not rename,
    external scripts depend on these values.
    """

    MO = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Region(Enum):
    """Enum for regions."""

    US = auto()
    EU = auto()
    APAC = auto()
    GLOBAL = auto()


class ServiceLevel(Enum):
    """Enum for service levels."""

    STANDARD = "Standard"
    PREMIUM = "Premium"
    PREMIER = "Premier"
    PREMIER_PLUS = "Premier Plus"
    MAX_SUCCESS = "Max Success"
