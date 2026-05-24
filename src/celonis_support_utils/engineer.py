from celonis_support_utils.shift import Shift

from .validators import parse_region, require_non_empty


class Engineer:
    """Class representing a support engineer."""

    def __init__(
        self,
        engineer_id: str,
        name: str,
        region: str,
        shift: Shift | None = None,
        open_ticket_count: int = 0,
    ):
        self.engineer_id = require_non_empty(engineer_id, "id")
        self.name = require_non_empty(name, "name")
        self.region = parse_region(region)
        self.shift = shift
        self.open_ticket_count = open_ticket_count

    def __repr__(self) -> str:
        return (
            f"Engineer(id={self.engineer_id}, name={self.name}, region={self.region})"
        )

    def is_on_shift(self) -> bool:
        """
        Returns True if the engineer is currently on shift.
        Returns False if no shift is assigned for today or if the shift is not active.
        """
        if self.shift is None:
            return False
        return self.shift.is_active()
