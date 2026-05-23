import pytest

from celonis_support_utils.payloads import (
    SalesforceCustomerPayload,
    SalesforceTicketPayload,
)


@pytest.fixture
def sample_engineer_data():
    return {"engineer_id": "1", "name": "Alice", "region": "US"}


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
        restriction="GLOBAL",
        service_level="STANDARD",
    )


@pytest.fixture
def sample_salesforce_customer_payload():
    return SalesforceCustomerPayload(company_name="Acme Corp", service_level="Premium")
