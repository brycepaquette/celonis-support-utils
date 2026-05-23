from enum import Enum

from celonis_support_utils.enums import Region, ServiceLevel
from celonis_support_utils.payloads import SalesforceTicketPayload


class IssueType(Enum):
    INCIDENT = "Incident"
    QUESTION = "Question"
    SERVICE_REQUEST = "Service Request"


class Ticket:
    def __init__(
        self,
        ticket_id: str,
        issue_type: str,
        severity: str,
        service: str,
        product_area: str,
        title: str,
        description: str,
        restriction: str,
        service_level: str,
    ):
        self.ticket_id = self._require_non_empty(ticket_id, "ticket_id")
        self.issue_type = self._parse_issue_type(issue_type)
        self.severity = self._require_non_empty(severity, "severity")
        self.service = self._require_non_empty(service, "service")
        self.product_area = self._require_non_empty(product_area, "product_area")
        self.title = self._require_non_empty(title, "title")
        self.description = self._require_non_empty(description, "description")
        self.restriction = self._parse_restriction(restriction)
        self.service_level = self._parse_service_level(service_level)

    def __repr__(self) -> str:
        return f"Ticket(ticket_id={self.ticket_id!r}, issue_type={self.issue_type!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ticket):
            return NotImplemented
        return self.ticket_id == other.ticket_id

    def __hash__(self) -> int:
        return hash(self.ticket_id)

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
    def _parse_restriction(value: str) -> Region:
        try:
            return Region[value.strip().upper()]
        except KeyError as exc:
            valid_regions = [region.name for region in Region]
            raise ValueError(
                f"Invalid restriction: {exc}. Must be one of {valid_regions}"
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
    def _require_non_empty(value: str, field_name: str) -> str:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()

    @classmethod
    def from_salesforce(cls, payload: SalesforceTicketPayload) -> "Ticket":
        return cls(
            ticket_id=payload["ticket_id"],
            issue_type=payload["issue_type"],
            severity=payload["severity"],
            service=payload["service"],
            product_area=payload["product_area"],
            title=payload["title"],
            description=payload["description"],
            restriction=payload["restriction"],
            service_level=payload["service_level"],
        )
