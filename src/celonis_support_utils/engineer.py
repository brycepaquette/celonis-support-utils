from celonis_support_utils.shift import Shift

from .enums import Region


class Engineer:
    def __init__(self, engineer_id: str, name: str, region: str):
        self.engineer_id = self._require_non_empty(engineer_id, "id")
        self.name = self._require_non_empty(name, "name")
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

    def _require_non_empty(self, value: str, field_name: str) -> str:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()

    def is_on_shift(self, assigned_shift: Shift | None) -> bool:
        """
        Returns True if the engineer is currently on shift.
        Returns False if no shift is assigned for today or if the shift is not active.
        """
        if assigned_shift is None:
            return False
        return assigned_shift.is_active()
