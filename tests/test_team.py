import pytest

from celonis_support_utils.engineer import Engineer
from celonis_support_utils.team import Team


@pytest.fixture
def sample_team_data(sample_engineer_data):
    return {
        "name": "Team A",
        "region": "US",
        "engineers": [Engineer(**sample_engineer_data)],
    }


def test_team_name_empty(sample_team_data):
    sample_team_data["name"] = ""
    with pytest.raises(ValueError, match="name cannot be empty"):
        Team(**sample_team_data)


def test_region_invalid(sample_team_data):
    sample_team_data["region"] = "InvalidRegion"
    with pytest.raises(ValueError) as exc_info:
        Team(**sample_team_data)
    assert "Invalid region" in str(exc_info.value)


def test_engineers_empty(sample_team_data):
    sample_team_data["engineers"] = []
    with pytest.raises(ValueError, match="Team must have at least one engineer"):
        Team(**sample_team_data)
