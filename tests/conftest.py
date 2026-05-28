import pytest

from celonis_support_utils.engineer import Engineer
from celonis_support_utils.payloads import (
    SalesforceCustomerPayload,
    SalesforceTicketPayload,
)
from celonis_support_utils.repository import InMemoryTicketRepository
from celonis_support_utils.shift import Shift
from celonis_support_utils.team import Team
from celonis_support_utils.ticket import Ticket

# --- Session-scoped fixtures ---


@pytest.fixture(scope="session")
def sample_always_on_shift():
    return Shift.from_raw(
        shift_id="shift1",
        start_time="00:00",
        end_time="00:00",
        timezone="America/New_York",
        active_days=["MO", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
    )


@pytest.fixture(scope="session")
def sample_engineer_on_shift(sample_always_on_shift):
    return Engineer(
        engineer_id="1",
        name="Alice",
        region="US",
        shift=sample_always_on_shift,
    )


@pytest.fixture(scope="session")
def sample_engineer_off_shift():
    return Engineer(
        engineer_id="2",
        name="Bob",
        region="US",
        shift=None,
    )


@pytest.fixture(scope="session")
def team_with_on_shift_engineer(sample_engineer_on_shift):
    return Team(name="Team US", region="US", engineers=[sample_engineer_on_shift])


@pytest.fixture(scope="session")
def team_with_off_shift_engineer(sample_engineer_off_shift):
    return Team(name="Team US", region="US", engineers=[sample_engineer_off_shift])


# --- Function-scoped fixtures (mutable — each test gets a fresh instance) ---


@pytest.fixture(scope="function")
def repo():
    return InMemoryTicketRepository()


@pytest.fixture(scope="function")
def sample_engineer_data():
    return {
        "engineer_id": "1",
        "name": "Alice",
        "region": "US",
    }


@pytest.fixture(scope="function")
def sample_salesforce_ticket_payload():
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
        assignee="Alice Baker",
        customer_id="1",
    )


@pytest.fixture(scope="function")
def sample_salesforce_ticket(sample_salesforce_ticket_payload):
    return Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)


@pytest.fixture(scope="function")
def sample_salesforce_customer_payload():
    return SalesforceCustomerPayload(
        customer_id="1", company_name="Acme Corp", service_level="Premium"
    )


# --- Parametrized fixtures ---


@pytest.fixture(
    params=[
        ("engineer_id", "", "id cannot be empty"),
        ("name", "", "name cannot be empty"),
        ("region", "INVALID_REGION", "Invalid region"),
    ],
    ids=["engineer_id", "name", "region"],
)
def invalid_engineer_field(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    params=[
        ("ticket_id", "", "ticket_id cannot be empty"),
        ("issue_type", "BadType", "Invalid issue type"),
        ("region", "BadRegion", "Invalid region"),
        ("service_level", "BadLevel", "Invalid service level"),
        ("severity", "BadSev", "Invalid severity"),
        ("status", "BadStatus", "Invalid status"),
        ("assignee", "", "assignee cannot be empty"),
    ],
    ids=[
        "ticket_id",
        "issue_type",
        "region",
        "service_level",
        "severity",
        "status",
        "assignee",
    ],
)
def invalid_ticket_field(request: pytest.FixtureRequest):
    return request.param
