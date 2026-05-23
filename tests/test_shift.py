from datetime import datetime

import pytest

from celonis_support_utils.shift import Shift


@pytest.fixture
def daytime_shift():
    return Shift.from_raw(
        shift_id="US-East-1",
        start_time="09:00",
        end_time="18:00",
        timezone="America/New_York",
        active_days=["MO", "TUE", "WED", "THU", "FRI"],  # Monday to Friday
    )


@pytest.fixture
def overnight_shift():
    return Shift.from_raw(
        shift_id="US-East-Overnight",
        start_time="22:00",
        end_time="07:00",
        timezone="America/New_York",
        active_days=["MO", "TUE", "WED", "THU", "FRI"],  # Monday to Friday
    )


def test_shift_is_active_during_hours(daytime_shift):
    assert daytime_shift.is_active(
        datetime(2024, 6, 3, 10, 0, tzinfo=daytime_shift.timezone)
    )  # Monday at 10:00


def test_shift_is_inactive_outside_hours(daytime_shift):
    assert not daytime_shift.is_active(
        datetime(2024, 6, 3, 8, 0, tzinfo=daytime_shift.timezone)
    )  # Monday at 08:00


def test_shift_is_inactive_on_weekend(daytime_shift):
    assert not daytime_shift.is_active(
        datetime(2024, 6, 8, 10, 0, tzinfo=daytime_shift.timezone)
    )  # Saturday at 10:00


def test_overnight_shift_is_active_during_hours(overnight_shift):
    assert overnight_shift.is_active(
        datetime(2024, 6, 3, 1, 0, tzinfo=overnight_shift.timezone)
    )  # Monday at 01:00


def test_overnight_shift_is_inactive_outside_hours(overnight_shift):
    assert not overnight_shift.is_active(
        datetime(2024, 6, 3, 21, 0, tzinfo=overnight_shift.timezone)
    )  # Monday at 21:00
