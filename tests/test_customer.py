import pytest
from celonis_support_utils.customer import Customer, ServiceLevel


def test_valid_service_level():
    customer = Customer(company_name="Acme Corp", service_level="Premium")
    assert customer.service_level == ServiceLevel.PREMIUM


def test_invalid_service_level():
    with pytest.raises(ValueError) as exc_info:
        Customer(company_name="Acme Corp", service_level="InvalidServiceLevel")
    assert "Invalid service level" in str(exc_info.value)


def test_service_level_case_insensitivity():
    customer = Customer(company_name="Acme Corp", service_level="premium")
    assert customer.service_level == ServiceLevel.PREMIUM


def test_service_level_with_spaces():
    customer = Customer(company_name="Acme Corp", service_level="Premier Plus")
    assert customer.service_level == ServiceLevel.PREMIER_PLUS


def test_customer_name_empty():
    with pytest.raises(ValueError) as exc_info:
        Customer(company_name="", service_level="Standard")
    assert "company_name cannot be empty" in str(exc_info.value)
