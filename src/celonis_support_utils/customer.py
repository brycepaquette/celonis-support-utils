from dataclasses import dataclass

from .enums import ServiceLevel
from .payloads import SalesforceCustomerPayload


@dataclass(frozen=True)
class Customer:
    """Represents a customer with a company name and service level."""

    company_name: str
    service_level: ServiceLevel

    def __post_init__(self) -> None:
        if not self.company_name.strip():
            raise ValueError("company_name cannot be empty")

    @classmethod
    def from_salesforce_payload(cls, payload: SalesforceCustomerPayload) -> "Customer":
        """Creates a Customer instance from a Salesforce payload."""
        return cls(
            company_name=payload["company_name"],
            service_level=Customer._parse_service_level(payload["service_level"]),
        )

    @staticmethod
    def _parse_service_level(value: str) -> ServiceLevel:
        try:
            return ServiceLevel[value.strip().replace(" ", "_").upper()]
        except KeyError as exc:
            valid_levels = [s.name for s in ServiceLevel]
            raise ValueError(
                f"Invalid service level: {exc}. Must be one of {valid_levels}"
            ) from exc
