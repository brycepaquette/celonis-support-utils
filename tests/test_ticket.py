import pytest

from celonis_support_utils.ticket import Severity, Ticket


def test_ticket_id_empty(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["ticket_id"] = ""
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "ticket_id cannot be empty" in str(exc_info.value)


def test_issue_type_invalid(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["issue_type"] = "InvalidType"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Invalid issue type" in str(exc_info.value)


def test_region_invalid(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["region"] = "InvalidRegion"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Invalid region" in str(exc_info.value)


def test_service_level_invalid(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["service_level"] = "InvalidLevel"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Invalid service level" in str(exc_info.value)


def test_severity_invalid(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["severity"] = "InvalidSeverity"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Invalid severity" in str(exc_info.value)


def test_no_severity_for_incident(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["severity"] = "-"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Severity is required for Incident tickets" in str(exc_info.value)


def test_no_severity_for_question(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["issue_type"] = "Question"
    sample_salesforce_ticket_payload["severity"] = "-"
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert ticket.severity is None


def test_status_invalid(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["status"] = "InvalidStatus"
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "Invalid status" in str(exc_info.value)


def test_assignee_empty(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["assignee"] = ""
    with pytest.raises(ValueError) as exc_info:
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert "assignee cannot be empty" in str(exc_info.value)


def test_from_salesforce_payload_valid(sample_salesforce_ticket_payload):
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert ticket.ticket_id == sample_salesforce_ticket_payload["ticket_id"]
    assert ticket.issue_type.name == sample_salesforce_ticket_payload[
        "issue_type"
    ].upper().replace(" ", "_")
    assert ticket.severity.name == sample_salesforce_ticket_payload[
        "severity"
    ].upper().replace(" ", "_")
    assert ticket.service == sample_salesforce_ticket_payload["service"]
    assert ticket.product_area == sample_salesforce_ticket_payload["product_area"]
    assert ticket.title == sample_salesforce_ticket_payload["title"]
    assert ticket.description == sample_salesforce_ticket_payload["description"]
    assert ticket.region.name == sample_salesforce_ticket_payload["region"].upper()
    assert ticket.service_level.name == sample_salesforce_ticket_payload[
        "service_level"
    ].upper().replace(" ", "_")
    assert ticket.status.name == sample_salesforce_ticket_payload[
        "status"
    ].upper().replace(" ", "_")
    assert ticket.assignee == sample_salesforce_ticket_payload["assignee"]


def test_ticket_equality(sample_salesforce_ticket_payload):
    ticket1 = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    ticket2 = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert ticket1 == ticket2


def test_ticket_inequality(sample_salesforce_ticket_payload):
    ticket1 = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    modified_payload = sample_salesforce_ticket_payload.copy()
    modified_payload["ticket_id"] = "TICKET-9999"
    ticket2 = Ticket.from_salesforce_payload(modified_payload)
    assert ticket1 != ticket2


def test_hashable(sample_salesforce_ticket_payload):
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    ticket_set = {ticket}
    assert ticket in ticket_set


def test_severity_change_fires_callback(sample_salesforce_ticket_payload):
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    calls = []

    def callback(old, new):
        calls.append((old, new))

    ticket.on_severity_change(callback)
    ticket.severity = Severity.SEV2
    assert len(calls) == 1
    assert calls[0] == (Severity.SEV1, Severity.SEV2)


def test_same_severity_does_not_fire_callback(sample_salesforce_ticket_payload):
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    calls = []

    def callback(old, new):
        calls.append((old, new))

    ticket.on_severity_change(callback)
    ticket.severity = Severity.SEV1  # Setting to the same severity
    assert (
        len(calls) == 0
    )  # Callback should not be called since severity did not actually change
