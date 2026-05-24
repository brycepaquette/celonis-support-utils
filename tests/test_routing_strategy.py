import pytest

from celonis_support_utils.engineer import Engineer
from celonis_support_utils.exceptions import NoAvailableEngineerError
from celonis_support_utils.routing_strategy import FallbackRouting, StandardRouting
from celonis_support_utils.team import Team
from celonis_support_utils.ticket import Ticket


class AlwaysFailStrategy:
    def route(self, ticket: Ticket, teams: list[Team]) -> Engineer:
        raise NoAvailableEngineerError(ticket, "always fails")


def test_standard_routing_picks_lowest_ticket_count(
    sample_always_on_shift, sample_salesforce_ticket_payload
):
    engineer1 = Engineer(
        engineer_id="1",
        name="Alice",
        region="US",
        shift=sample_always_on_shift,
        open_ticket_count=5,
    )
    engineer2 = Engineer(
        engineer_id="2",
        name="Bob",
        region="US",
        shift=sample_always_on_shift,
        open_ticket_count=2,
    )
    routing_strategy = StandardRouting()
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    teams = [Team(name="Team US", region="US", engineers=[engineer1, engineer2])]
    assigned = routing_strategy.route(ticket, teams)
    assert assigned == engineer2


def test_no_engineers_available(sample_salesforce_ticket_payload):
    engineer = Engineer(
        engineer_id="1", name="Alice", region="US"
    )  # no shift = off shift
    routing_strategy = StandardRouting()
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    teams = [Team(name="Team US", region="US", engineers=[engineer])]
    with pytest.raises(NoAvailableEngineerError) as exc_info:
        routing_strategy.route(ticket, teams)
    assert (
        str(exc_info.value)
        == f"No available engineer for ticket {ticket.ticket_id!r}: "
        "No engineers currently on shift"
    )


def test_fallback_routing_both_fail(
    sample_engineer_off_shift, sample_salesforce_ticket_payload
):
    routing_strategy = StandardRouting()
    fallback_strategy = StandardRouting()  # Both strategies are the same for this test
    combined_strategy = FallbackRouting(
        primary=routing_strategy, secondary=fallback_strategy
    )
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    teams = [Team(name="Team US", region="US", engineers=[sample_engineer_off_shift])]
    with pytest.raises(NoAvailableEngineerError) as exc_info:
        combined_strategy.route(ticket, teams)
    assert (
        str(exc_info.value)
        == f"No available engineer for ticket {ticket.ticket_id!r}: "
        "No engineers available in either primary or secondary strategy"
    )


def test_fallback_routing_primary_succeeds(
    sample_engineer_on_shift, sample_salesforce_ticket_payload
):
    primary_strategy = StandardRouting()
    secondary_strategy = AlwaysFailStrategy()
    combined_strategy = FallbackRouting(
        primary=primary_strategy, secondary=secondary_strategy
    )
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    teams = [Team(name="Team US", region="US", engineers=[sample_engineer_on_shift])]
    assigned = combined_strategy.route(ticket, teams)
    assert assigned == sample_engineer_on_shift


def test_fallback_routing_primary_fails_secondary_succeeds(
    sample_engineer_off_shift,
    sample_engineer_on_shift,
    sample_salesforce_ticket_payload,
):
    primary_strategy = AlwaysFailStrategy()
    secondary_strategy = StandardRouting()
    combined_strategy = FallbackRouting(
        primary=primary_strategy, secondary=secondary_strategy
    )
    ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    teams = [
        Team(name="Team US", region="US", engineers=[sample_engineer_off_shift]),
        Team(name="Team US", region="US", engineers=[sample_engineer_on_shift]),
    ]
    assigned = combined_strategy.route(ticket, teams)
    assert assigned == sample_engineer_on_shift
