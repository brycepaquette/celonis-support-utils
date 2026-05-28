from unittest.mock import MagicMock

import pytest

from celonis_support_utils.ticket import Severity, Ticket


def test_ticket_field_validation(
    sample_salesforce_ticket_payload, invalid_ticket_field
):
    field, value, match = invalid_ticket_field
    sample_salesforce_ticket_payload[field] = value
    with pytest.raises(ValueError, match=match):
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)


def test_no_severity_for_incident(sample_salesforce_ticket_payload):
    sample_salesforce_ticket_payload["severity"] = "-"
    with pytest.raises(ValueError, match="Severity is required for Incident tickets"):
        Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)


@pytest.mark.parametrize(
    "severity_str, expected_severity",
    [
        ("Sev1", Severity.SEV1),
        ("sev2", Severity.SEV2),
        ("SEV3", Severity.SEV3),
        ("SEV4", Severity.SEV4),
        ("-", None),
    ],
)
def test_severity_parsing(
    sample_salesforce_ticket_payload, severity_str, expected_severity
):
    sample_salesforce_ticket_payload["issue_type"] = (
        "Question" if severity_str == "-" else "Incident"
    )
    sample_salesforce_ticket_payload["severity"] = severity_str
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    assert ticket.severity == expected_severity


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
    mock_callback = MagicMock()
    ticket.on_severity_change(mock_callback)
    ticket.severity = Severity.SEV2
    mock_callback.assert_called_once_with(Severity.SEV1, Severity.SEV2)


def test_same_severity_does_not_fire_callback(sample_salesforce_ticket_payload):
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    mock_callback = MagicMock()

    ticket.on_severity_change(mock_callback)
    ticket.severity = Severity.SEV1  # Setting to the same severity
    mock_callback.assert_not_called()
