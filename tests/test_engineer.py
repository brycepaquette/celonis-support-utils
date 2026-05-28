import pytest

from celonis_support_utils.engineer import Engineer


def test_engineer_field_validation(sample_engineer_data, invalid_engineer_field):
    field, value, match = invalid_engineer_field
    sample_engineer_data[field] = value
    with pytest.raises(ValueError, match=match):
        Engineer(**sample_engineer_data)


def test_is_on_shift(sample_engineer_on_shift):
    assert sample_engineer_on_shift.is_on_shift()
