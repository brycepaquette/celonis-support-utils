from celonis_support_utils.enums import ServiceLevel


class Customer:
    def __init__(self, company_name: str, service_level: str):
        if not company_name.strip():
            raise ValueError("company_name cannot be empty")
        self.company_name = company_name
        self.service_level = self._parse_service_level(service_level)

    @staticmethod
    def _parse_service_level(value: str) -> ServiceLevel:
        try:
            return ServiceLevel[value.strip().replace(" ", "_").upper()]
        except KeyError as exc:
            valid_levels = [s.name for s in ServiceLevel]
            raise ValueError(
                f"Invalid service level: {exc}. Must be one of {valid_levels}"
            ) from exc
