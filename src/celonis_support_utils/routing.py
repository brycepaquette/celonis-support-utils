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
    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
        eligible_teams = [
            team for team in teams if ticket.restriction in (Region.GLOBAL, team.region)
        ]
        for team in eligible_teams:
            for engineer in team.engineers:
                if engineer.is_on_shift():
                    return engineer
        return None


class EscalationRouting:
    """
    Escalation routing: finds the most senior engineer regardless of shift.
    TODO: Requires Engineer seniority levels (L1/L2) and product area matching.
    """

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
        raise NotImplementedError
