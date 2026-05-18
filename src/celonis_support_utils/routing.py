from typing import Protocol

from celonis_support_utils.enums import Region

from .engineer import Engineer
from .team import Team
from .ticket import Ticket


class RoutingStrategy(Protocol):
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
                # TODO: Implement shift assignment logic here.
                assigned_shift = None
                if engineer.is_on_shift(assigned_shift):
                    return engineer
        return None


class EscalationRouting:
    """TODO: Implement escalation routing logic."""

    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer | None:
        raise NotImplementedError
