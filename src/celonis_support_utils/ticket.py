from collections.abc import Callable
from enum import Enum, auto

from celonis_support_utils.enums import ServiceLevel
from celonis_support_utils.payloads import SalesforceTicketPayload

from .validators import parse_region, require_non_empty


class IssueType(Enum):
    """Defines the type of issue for a support ticket."""

    INCIDENT = "Incident"
    QUESTION = "Question"
    SERVICE_REQUEST = "Service Request"


class Severity(Enum):
    """Defines the severity levels for support tickets."""

    SEV1 = auto()
    SEV2 = auto()
    SEV3 = auto()
    SEV4 = auto()


class Ticket:
    """Represents a support ticket with various attributes and behaviors."""

    def __init__(
        self,
        ticket_id: str,
        issue_type: str,
        severity: str,
        service: str,
        product_area: str,
        title: str,
        description: str,
        region: str,
        service_level: str,
        status: str,
    ):
        self._severity_callbacks: list[Callable[[Severity, Severity], None]] = []
        self.ticket_id = require_non_empty(ticket_id, "ticket_id")
        self.issue_type = self._parse_issue_type(issue_type)
        self._severity = self._parse_severity(severity)
        self.service = require_non_empty(service, "service")
        self.product_area = require_non_empty(product_area, "product_area")
        self.title = require_non_empty(title, "title")
        self.description = require_non_empty(description, "description")
        self.region = parse_region(region)
        self.service_level = self._parse_service_level(service_level)
        self.status = require_non_empty(status, "status")

    def __repr__(self) -> str:
        return f"Ticket(ticket_id={self.ticket_id!r}, issue_type={self.issue_type!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ticket):
            return NotImplemented
        return self.ticket_id == other.ticket_id

    def __hash__(self) -> int:
        return hash(self.ticket_id)

    @property
    def severity(self) -> Severity:
        """Gets the current severity of the ticket."""
        return self._severity

    @severity.setter
    def severity(self, new_severity: Severity) -> None:
        """Sets a new severity for the ticket and triggers callbacks if it changes."""
        if self._severity == new_severity:
            return
        old_severity = self._severity
        self._severity = new_severity
        for callback in self._severity_callbacks:
            callback(old_severity, new_severity)

    def on_severity_change(
        self, callback: Callable[[Severity, Severity], None]
    ) -> None:
        """Registers a callback to be called when the severity changes."""
        self._severity_callbacks.append(callback)

    @classmethod
    def from_salesforce_payload(cls, payload: SalesforceTicketPayload) -> "Ticket":
        """Creates a Ticket instance from a SalesforceTicketPayload."""
        if payload["issue_type"] == "Incident" and not payload["severity"]:
            raise ValueError("Severity is required for Incident tickets")

        return cls(
            ticket_id=payload["ticket_id"],
            issue_type=payload["issue_type"],
            severity=payload["severity"],
            service=payload["service"],
            product_area=payload["product_area"],
            title=payload["title"],
            description=payload["description"],
            region=payload["region"],
            service_level=payload["service_level"],
            status=payload["status"],
        )

    @staticmethod
    def _parse_issue_type(value: str) -> IssueType:
        try:
            return IssueType[value.strip().upper().replace(" ", "_")]
        except KeyError as exc:
            valid_types = [issue_type.name for issue_type in IssueType]
            raise ValueError(
                f"Invalid issue type: {exc}. Must be one of {valid_types}"
            ) from exc

    @staticmethod
    def _parse_service_level(value: str) -> ServiceLevel:
        try:
            return ServiceLevel[value.strip().upper().replace(" ", "_")]
        except KeyError as exc:
            valid_levels = [level.name for level in ServiceLevel]
            raise ValueError(
                f"Invalid service level: {exc}. Must be one of {valid_levels}"
            ) from exc

    @staticmethod
    def _parse_severity(value: str) -> Severity:
        try:
            return Severity[value.strip().upper()]
        except KeyError as exc:
            valid_severities = [severity.name for severity in Severity]
            raise ValueError(
                f"Invalid severity: {exc}. Must be one of {valid_severities}"
            ) from exc
