from enum import Enum

from celonis_support_utils.enums import Region


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
    ):
        self.ticket_id = ticket_id
        self.issue_type = self._parse_issue_type(issue_type)
        self.severity = severity
        self.service = service
        self.product_area = product_area
        self.title = title
        self.description = description
        self.restriction = self._parse_restriction(restriction)

    @staticmethod
    def _parse_issue_type(value: str) -> IssueType:
        try:
            return IssueType[value.strip().upper().replace(" ", "_")]
        except KeyError as exc:
            valid_types = [t.name for t in IssueType]
            raise ValueError(
                f"Invalid issue type: {exc}. Must be one of {valid_types}"
            ) from exc

    @staticmethod
    def _parse_restriction(value: str) -> Region:
        try:
            return Region[value.strip().upper()]
        except KeyError as exc:
            valid_regions = [r.name for r in Region]
            raise ValueError(
                f"Invalid restriction: {exc}. Must be one of {valid_regions}"
            ) from exc
