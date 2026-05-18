from enum import Enum


class ServiceLevel(Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"
    PREMIER = "Premier"
    PREMIER_PLUS = "Premier Plus"
    MAXSUCCESS = "MaxSuccess"


class Customer:
    def __init__(self, company_name: str, service_level: ServiceLevel):
        self.company_name = company_name
        self.service_level = service_level
