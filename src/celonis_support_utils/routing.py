from typing import Protocol

from celonis_support_utils.enums import Region

from .engineer import Engineer
from .team import Team
from .ticket import Ticket


class RoutingStrategy(Protocol):
    """
    Protocol chosen over ABC: routing implementations should not need to import
    from this codebase — any class with a matching route() signature qualifies
    automatically. This allows third-party or external routing strategies to
    plug in without inheritance.
    """

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
        """
        Determines which engineer should be assigned to the given ticket based
        on the routing strategy.
        Returns the assigned Engineer or None if no suitable engineer is found.
        """
        ...


class StandardRouting:
    """Standard routing strategy."""

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
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
            return None
        return min(on_shift, key=lambda e: e.open_ticket_count)


class EscalationRouting:
    """
    Escalation routing: finds the most senior engineer regardless of shift.
    TODO: Requires Engineer seniority levels (L1/L2) and product area matching.
    """

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
        raise NotImplementedError
