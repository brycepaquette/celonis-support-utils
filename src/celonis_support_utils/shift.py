from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo

from .enums import DayOfWeek


@dataclass(frozen=True)
class Shift:
    """Represents a work shift with specific active days and times."""

    shift_id: str
    start_time: time
    end_time: time
    timezone: ZoneInfo
    active_days: tuple[DayOfWeek, ...]

    def is_active(self, now: datetime | None = None) -> bool:
        """Checks if the shift is currently active based on the current time and day."""
        if now is None:
            now = datetime.now(self.timezone)
        elif now.tzinfo is not None:
            now = now.astimezone(self.timezone)

        current_day = DayOfWeek(now.weekday())
        current_time = now.time()

        if current_day not in self.active_days:
            return False
        if self.start_time <= self.end_time:
            return self.start_time <= current_time < self.end_time
        else:
            # Shift spans midnight
            return current_time >= self.start_time or current_time < self.end_time

    @classmethod
    def from_raw(
        cls,
        shift_id: str,
        start_time: str,
        end_time: str,
        timezone: str,
        active_days: list[str],
    ) -> "Shift":
        """Creates a Shift instance from raw string inputs."""
        return cls(
            shift_id=shift_id,
            start_time=cls._parse_time(start_time),
            end_time=cls._parse_time(end_time),
            timezone=cls._parse_timezone(timezone),
            active_days=tuple(cls._parse_active_days(active_days)),
        )

    @staticmethod
    def _parse_time(value: str) -> time:
        try:
            return time.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("Time must be in HH:MM format") from exc

    @staticmethod
    def _parse_timezone(value: str) -> ZoneInfo:
        try:
            return ZoneInfo(value)
        except KeyError as exc:
            raise ValueError("Timezone must be a valid IANA timezone") from exc

    @staticmethod
    def _parse_active_days(values: list[str]) -> list[DayOfWeek]:
        try:
            return [DayOfWeek[day.strip()] for day in values]
        except KeyError as exc:
            valid_days = [d.name for d in DayOfWeek]
            raise ValueError(
                f"Invalid day: {exc}. Must be one of {valid_days}"
            ) from exc
