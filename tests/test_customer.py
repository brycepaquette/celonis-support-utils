import pytest

from celonis_support_utils.customer import Customer, ServiceLevel


def test_service_level_valid(sample_salesforce_customer_payload):
    customer = Customer.from_salesforce_payload(sample_salesforce_customer_payload)
    assert customer.service_level == ServiceLevel.PREMIUM


def test_service_level_invalid(sample_salesforce_customer_payload):
    with pytest.raises(ValueError) as exc_info:
        Customer.from_salesforce_payload(
            {**sample_salesforce_customer_payload, "service_level": "InvalidLevel"}
        )
    assert "Invalid service level" in str(exc_info.value)


def test_service_level_case_insensitivity(sample_salesforce_customer_payload):
    customer = Customer.from_salesforce_payload(
        {**sample_salesforce_customer_payload, "service_level": "premium"}
    )
    assert customer.service_level == ServiceLevel.PREMIUM


def test_service_level_with_spaces(sample_salesforce_customer_payload):
    customer = Customer.from_salesforce_payload(
        {**sample_salesforce_customer_payload, "service_level": "Premier Plus"}
    )
    assert customer.service_level == ServiceLevel.PREMIER_PLUS


def test_customer_name_empty(sample_salesforce_customer_payload):
    with pytest.raises(ValueError) as exc_info:
        Customer.from_salesforce_payload(
            {**sample_salesforce_customer_payload, "company_name": "   "}
        )
    assert "company_name cannot be empty" in str(exc_info.value)


def test_customer_id_empty(sample_salesforce_customer_payload):
    with pytest.raises(ValueError) as exc_info:
        Customer.from_salesforce_payload(
            {**sample_salesforce_customer_payload, "customer_id": "   "}
        )
    assert "customer_id cannot be empty" in str(exc_info.value)
