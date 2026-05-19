import pytest
from celonis_support_utils.engineer import Engineer


@pytest.fixture
def sample_engineer_data():
    return {"engineer_id": "1", "name": "Alice", "region": "US"}


def test_engineer_id_non_empty(sample_engineer_data):
    sample_engineer_data["engineer_id"] = ""
    with pytest.raises(ValueError, match="id cannot be empty"):
        Engineer(**sample_engineer_data)


def test_name_non_empty(sample_engineer_data):
    sample_engineer_data["name"] = ""
    with pytest.raises(ValueError, match="name cannot be empty"):
        Engineer(**sample_engineer_data)


def test_region_invalid(sample_engineer_data):
    sample_engineer_data["region"] = "INVALID_REGION"
    with pytest.raises(ValueError, match="Invalid region"):
        Engineer(**sample_engineer_data)


def test_is_on_shift(sample_engineer_data):
    engineer = Engineer(**sample_engineer_data)
    assert not engineer.is_on_shift(None)
