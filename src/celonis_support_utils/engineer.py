from celonis_support_utils.shift import Shift

from .enums import Region


class Engineer:
    def __init__(self, id: int, name: str, region: str):
        self.id = id
        self.name = name
        self.region = self._parse_region(region)

    @staticmethod
    def _parse_region(value: str) -> Region:
        try:
            return Region[value.strip().upper()]
        except KeyError as exc:
            valid_regions = [r.name for r in Region]
            raise ValueError(
                f"Invalid region: {exc}. Must be one of {valid_regions}"
            ) from exc

    def is_on_shift(self, assigned_shift: Shift | None) -> bool:
        """
        Returns True if the engineer is currently on shift.
        Returns False if no shift is assigned for today or if the shift is not active.
        """
        if assigned_shift is None:
            return False
        return assigned_shift.is_active()
