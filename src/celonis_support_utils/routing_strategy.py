from typing import Protocol

from .engineer import Engineer
from .enums import Region
from .exceptions import NoAvailableEngineerError
from .team import Team
from .ticket import Ticket


class RoutingStrategy(Protocol):
    """
    Protocol chosen over ABC: routing implementations should not need to import
    from this codebase — any class with a matching route() signature qualifies
    automatically. This allows third-party or external routing strategies to
    plug in without inheritance.
    """

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        """
        Determines which engineer should be assigned to the given ticket based
        on the routing strategy. Returns the assigned Engineer or raises
        NoAvailableEngineerError if no suitable engineer is found.
        """
        ...


class StandardRouting:
    """Standard routing strategy."""

    def __repr__(self) -> str:
        return "StandardRouting()"

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        """Finds the available on-shift engineer with the lowest open ticket count."""
        eligible_teams = [
            team for team in teams if ticket.region in (Region.GLOBAL, team.region)
        ]
        on_shift = [
            engineer
            for team in eligible_teams
            for engineer in team.engineers
            if engineer.is_on_shift()
        ]
        if not on_shift:
            raise NoAvailableEngineerError(
                ticket,
                reason="No engineers currently on shift",
            )
        return min(on_shift, key=lambda e: e.open_ticket_count)


class EscalationRouting:
    """Escalation routing: routes to the L2 engineer currently on-call."""

    def __repr__(self) -> str:
        return "EscalationRouting()"

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        raise NotImplementedError


class FallbackRouting:
    """
    Fallback routing: retries a primary strategy, then falls back
    to a secondary if the first fails. Useful for implementing a
    simple retry mechanism or for combining multiple strategies.
    """

    def __init__(self, primary: RoutingStrategy, secondary: RoutingStrategy):
        self.primary = primary
        self.secondary = secondary

    def __repr__(self) -> str:
        return (
            f"FallbackRouting(primary={self.primary!r}, secondary={self.secondary!r})"
        )

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        try:
            return self.primary.route(ticket, teams)
        except NoAvailableEngineerError:
            try:
                return self.secondary.route(ticket, teams)
            except NoAvailableEngineerError as exc:
                raise NoAvailableEngineerError(
                    ticket,
                    reason="No engineers available in either primary or"
                    " secondary strategy",
                ) from exc
