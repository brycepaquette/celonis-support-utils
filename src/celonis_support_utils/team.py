from .engineer import Engineer
from .validators import parse_region, require_non_empty


class Team:
    """Class representing a support team."""

    def __init__(self, name: str, region: str, engineers: list[Engineer]):
        if not engineers:
            raise ValueError("Team must have at least one engineer")
        self.name = require_non_empty(name, "name")
        self.region = parse_region(region)
        self.engineers = engineers
