import pytest
from celonis_support_utils.ticket import Ticket


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


def test_ticket_id_empty(sample_ticket_data):
    sample_ticket_data["ticket_id"] = ""
    with pytest.raises(ValueError) as exc_info:
        Ticket(**sample_ticket_data)
    assert "ticket_id cannot be empty" in str(exc_info.value)


def test_severity_empty(sample_ticket_data):
    sample_ticket_data["severity"] = ""
    with pytest.raises(ValueError) as exc_info:
        Ticket(**sample_ticket_data)
    assert "severity cannot be empty" in str(exc_info.value)


def test_issue_type_invalid(sample_ticket_data):
    sample_ticket_data["issue_type"] = "InvalidType"
    with pytest.raises(ValueError) as exc_info:
        Ticket(**sample_ticket_data)
    assert "Invalid issue type" in str(exc_info.value)


def test_restriction_invalid(sample_ticket_data):
    sample_ticket_data["restriction"] = "InvalidRegion"
    with pytest.raises(ValueError) as exc_info:
        Ticket(**sample_ticket_data)
    assert "Invalid restriction" in str(exc_info.value)


def test_service_level_invalid(sample_ticket_data):
    sample_ticket_data["service_level"] = "InvalidLevel"
    with pytest.raises(ValueError) as exc_info:
        Ticket(**sample_ticket_data)
    assert "Invalid service level" in str(exc_info.value)
