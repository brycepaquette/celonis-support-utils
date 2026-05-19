import pytest


@pytest.fixture
def sample_engineer_data():
    return {"engineer_id": "1", "name": "Alice", "region": "US"}


@pytest.fixture
def sample_ticket_data():
    return {
        "ticket_id": "TICKET-123",
        "issue_type": "Incident",
        "severity": "SEV1",
        "service": "Data Integration",
        "product_area": "Connectors",
        "title": "Data Connector Failure",
        "description": "The data connector is failing to sync.",
        "restriction": "EU",
        "service_level": "STANDARD",
    }
