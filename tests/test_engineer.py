import pytest

from celonis_support_utils.engineer import Engineer


def test_engineer_id_empty(sample_engineer_data):
    sample_engineer_data["engineer_id"] = ""
    with pytest.raises(ValueError, match="id cannot be empty"):
        Engineer(**sample_engineer_data)


def test_name_empty(sample_engineer_data):
    sample_engineer_data["name"] = ""
    with pytest.raises(ValueError, match="name cannot be empty"):
        Engineer(**sample_engineer_data)


def test_region_invalid(sample_engineer_data):
    sample_engineer_data["region"] = "INVALID_REGION"
    with pytest.raises(ValueError, match="Invalid region"):
        Engineer(**sample_engineer_data)


def test_is_on_shift(sample_engineer_active_shift):
    assert sample_engineer_active_shift.is_on_shift()
