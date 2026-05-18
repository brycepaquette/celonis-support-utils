from celonis_support_utils.shift import Shift

from .enums import Region


class Engineer:
    def __init__(self, id: int, name: str, region: str, level: str):
        self.id = id
        self.name = name
        self.region = self._parse_region(region)
        self.level = level

    @staticmethod
    def _parse_region(value: str) -> Region:
        try:
            return Region[value.strip().upper()]
        except KeyError as exc:
            valid_regions = [r.name for r in Region]
            raise ValueError(
                f"Invalid region: {exc}. Must be one of {valid_regions}"
            ) from exc

    def is_on_shift(self, shift: Shift) -> bool:
        return shift.is_active()
