from .ticket import Ticket


class NoAvailableEngineerError(Exception):
    """Raised when no on-shift engineer can be found for a ticket."""

    def __init__(self, ticket: Ticket, reason: str):
        self.ticket = ticket
        self.reason = reason
        super().__init__(
            f"No available engineer for ticket {ticket.ticket_id!r}: {reason}"
        )
