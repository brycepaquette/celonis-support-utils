import pytest

from celonis_support_utils.engineer import Engineer
from celonis_support_utils.payloads import (
    SalesforceCustomerPayload,
    SalesforceTicketPayload,
)
from celonis_support_utils.shift import Shift


@pytest.fixture
def sample_engineer_data():
    return {
        "engineer_id": "1",
        "name": "Alice",
        "region": "US",
    }


@pytest.fixture
def sample_engineer_active_shift(sample_always_on_shift):
    return Engineer(
        engineer_id="1",
        name="Alice",
        region="US",
        shift=sample_always_on_shift,
    )


@pytest.fixture
def sample_always_on_shift():
    return Shift.from_raw(
        shift_id="shift1",
        start_time="00:00",
        end_time="23:59",
        timezone="America/New_York",
        active_days=["MO", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
    )


@pytest.fixture
def sample_salesforce_payload():
    return SalesforceTicketPayload(
        ticket_id="123",
        issue_type="Incident",
        severity="SEV1",
        service="AI / Machine Learning",
        product_area="PyCelonis",
        title="PyCelonis Failure",
        description="PyCelonis is failing to sync.",
        region="GLOBAL",
        service_level="STANDARD",
        status="In Progress",
    )


@pytest.fixture
def sample_salesforce_customer_payload():
    return SalesforceCustomerPayload(company_name="Acme Corp", service_level="Premium")
