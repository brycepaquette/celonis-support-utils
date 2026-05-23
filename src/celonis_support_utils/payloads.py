from typing import TypedDict


class SalesforceTicketPayload(TypedDict):
    ticket_id: str
    issue_type: str
    severity: str
    service: str
    product_area: str
    title: str
    description: str
    restriction: str
    service_level: str
