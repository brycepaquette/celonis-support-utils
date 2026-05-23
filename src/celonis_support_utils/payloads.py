from typing import Literal, TypedDict


class SalesforceTicketPayload(TypedDict):
    ticket_id: str
    issue_type: Literal["Incident", "Question", "Service Request"]
    severity: Literal["SEV1", "SEV2", "SEV3", "SEV4"]
    service: str
    product_area: str
    title: str
    description: str
    region: Literal["Global", "EU", "US", "APAC"]
    service_level: Literal[
        "Standard", "Premium", "Premier", "Premier Plus", "Max Success"
    ]


class SalesforceCustomerPayload(TypedDict):
    company_name: str
    service_level: Literal[
        "Standard", "Premium", "Premier", "Premier Plus", "Max Success"
    ]
