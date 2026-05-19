from .engineer import Engineer
from .enums import Region


class Team:
    def __init__(self, name: str, region: str, engineers: list[Engineer]):
        if not engineers:
            raise ValueError("Team must have at least one engineer")
        self.name = self._require_non_empty(name, "name")
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

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()
