from .engineer import Engineer
from .enums import Region


class Team:
    def __init__(self, name: str, region: str, engineers: list[Engineer]):
        self.name = name
        self.region = self._parse_region(region)
        self.engineers = engineers

    @staticmethod
    def _parse_region(value: str) -> Region:
        try:
            return Region[value.strip().upper()]
        except KeyError as exc:
            valid_regions = [r.name for r in Region]
            raise ValueError(
                f"Invalid region: {exc}. Must be one of {valid_regions}"
            ) from exc
