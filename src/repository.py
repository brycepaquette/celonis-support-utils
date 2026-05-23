from typing import Protocol

from celonis_support_utils.ticket import Ticket


class TicketRepository(Protocol):
    def save(self, ticket: Ticket) -> None: ...

    def get_by_id(self, ticket_id: str) -> Ticket | None: ...

    def list_open(self) -> list[Ticket]: ...


class SalesforceTicketRepository:
    # TODO: Implement SalesforceTicketRepository using Salesforce API
    def save(self, ticket: Ticket) -> None:
        raise NotImplementedError

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        raise NotImplementedError

    def list_open(self) -> list[Ticket]:
        raise NotImplementedError
