from typing import Protocol

from .ticket import Ticket, TicketStatus


class TicketRepository(Protocol):
    """Interface for a ticket repository."""

    def save(self, ticket: Ticket) -> None: ...

    def get_by_id(self, ticket_id: str) -> Ticket | None: ...

    def list_open(self) -> list[Ticket]: ...


class SalesforceTicketRepository:
    """Salesforce implementation of the TicketRepository interface."""

    # TODO: Implement SalesforceTicketRepository using Salesforce API

    def __repr__(self) -> str:
        return "SalesforceTicketRepository()"

    def save(self, ticket: Ticket) -> None:
        """Saves a ticket to the repository."""
        raise NotImplementedError

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        """Retrieves a ticket by its ID."""
        raise NotImplementedError

    def list_open(self) -> list[Ticket]:
        """Lists all open tickets."""
        raise NotImplementedError


class InMemoryTicketRepository:
    """In-memory implementation of the TicketRepository interface."""

    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}

    def __repr__(self) -> str:
        return f"InMemoryTicketRepository(tickets={len(self._tickets)})"

    def save(self, ticket: Ticket) -> None:
        """Saves a ticket to the repository."""
        self._tickets[ticket.ticket_id] = ticket

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        """Retrieves a ticket by its ID."""
        return self._tickets.get(ticket_id)

    def list_open(self) -> list[Ticket]:
        """Lists all open tickets."""
        return [
            ticket
            for ticket in self._tickets.values()
            if ticket.status != TicketStatus.CLOSED
        ]
