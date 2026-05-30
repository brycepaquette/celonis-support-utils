from argparse import ArgumentParser

from .engineer import Engineer
from .repository import InMemoryTicketRepository
from .routing_engine import RoutingEngine
from .routing_strategy import EscalationRouting, RoutingStrategy, StandardRouting
from .shift import Shift
from .team import Team
from .ticket import Ticket


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Celonis Support Utils")
    subparsers = parser.add_subparsers(dest="command", required=True)

    route_parser = subparsers.add_parser("route", help="Route a Celonis ticket")
    route_parser.add_argument(
        "ticket_id",
        type=str,
        help="The ID of the Celonis ticket to route",
    )
    route_parser.add_argument(
        "--strategy",
        type=str,
        choices=["standard", "escalation"],
        default="standard",
        required=False,
        help="The routing strategy to use for the Celonis ticket",
    )

    return parser


def _build_sample_teams() -> list[Team]:
    shift = Shift.from_raw(
        shift_id="EU-Day",
        start_time="00:00",
        end_time="00:00",
        timezone="Europe/Berlin",
        active_days=["MO", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
    )

    engineer = Engineer(
        engineer_id="1", name="John Doe", region="EU", shift=shift, open_ticket_count=5
    )
    return [Team(name="Sample Team", region="EU", engineers=[engineer])]


def _build_sample_ticket(ticket_id: str) -> Ticket:
    return Ticket.from_salesforce_payload(
        {
            "ticket_id": ticket_id,
            "issue_type": "Incident",
            "severity": "SEV1",
            "service": "Celonis EMS",
            "product_area": "Execution Management System",
            "title": "Sample Ticket",
            "description": "This is a sample ticket for testing purposes.",
            "region": "EU",
            "service_level": "Standard",
            "status": "New",
            "assignee": "",
            "customer_id": "C-001",
        }
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "route":
        print(f"Routing ticket {args.ticket_id} using {args.strategy} strategy")
        teams = _build_sample_teams()
        ticket = _build_sample_ticket(args.ticket_id)
        strategies: dict[str, RoutingStrategy] = {
            "standard": StandardRouting(),
            "escalation": EscalationRouting(),
        }
        engine = RoutingEngine(
            strategy=strategies[args.strategy], repo=InMemoryTicketRepository()
        )
        try:
            assignee = engine.assign(ticket, teams)
            print(f"Assigned ticket {ticket.ticket_id} to engineer {assignee.name}")
        except NotImplementedError:
            print(
                "escalation routing requires on-call schedule "
                "integration and is not yet implemented"
            )
            return 1
    return 0
