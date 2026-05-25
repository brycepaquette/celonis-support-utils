from typing import Literal, TypedDict


class SalesforceTicketPayload(TypedDict):
    """Payload for creating a ticket in Salesforce."""

    ticket_id: str
    issue_type: Literal["Incident", "Question", "Service Request"]
    severity: Literal["-", "SEV1", "SEV2", "SEV3", "SEV4"]
    service: str
    product_area: str
    title: str
    description: str
    region: Literal["Global", "EU", "US", "APAC"]
    service_level: Literal[
        "Standard", "Premium", "Premier", "Premier Plus", "Max Success"
    ]
    status: Literal["New", "In Progress", "On Hold", "Solution Provided", "Closed"]
    assignee: str
    customer_id: str


class SalesforceCustomerPayload(TypedDict):
    """Payload for creating a customer in Salesforce."""

    customer_id: str
    company_name: str
    service_level: Literal[
        "Standard", "Premium", "Premier", "Premier Plus", "Max Success"
    ]
