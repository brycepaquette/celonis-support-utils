from .engineer import Engineer
from .repository import TicketRepository
from .routing_strategy import RoutingStrategy
from .team import Team
from .ticket import Ticket


class RoutingEngine:
    """Assigns incoming tickets to engineers via a routing strategy."""

    def __init__(self, strategy: RoutingStrategy, repo: TicketRepository) -> None:
        self.strategy = strategy
        self.repo = repo

    def __repr__(self) -> str:
        return f"RoutingEngine(strategy={self.strategy.__class__.__name__!r})"

    def assign(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        engineer = self.strategy.route(ticket, teams)
        ticket.assignee = engineer.name
        self.repo.save(ticket)
        return engineer

    def swap_strategy(self, new_strategy: RoutingStrategy) -> None:
        self.strategy = new_strategy
