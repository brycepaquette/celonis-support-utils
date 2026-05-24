import pytest

from celonis_support_utils.engineer import Engineer
from celonis_support_utils.exceptions import NoAvailableEngineerError
from celonis_support_utils.routing_strategy import StandardRouting
from celonis_support_utils.team import Team
from celonis_support_utils.ticket import Ticket


def test_standard_routing_picks_lowest_ticket_count(
    sample_always_on_shift, sample_salesforce_payload
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
    ticket = Ticket.from_salesforce_payload(sample_salesforce_payload)
    teams = [Team(name="Team US", region="US", engineers=[engineer1, engineer2])]
    assigned = routing_strategy.route(ticket, teams)
    assert assigned == engineer2


def test_no_engineers_available(sample_salesforce_payload):
    engineer = Engineer(
        engineer_id="1", name="Alice", region="US"
    )  # no shift = off shift
    routing_strategy = StandardRouting()
    ticket = Ticket.from_salesforce_payload(sample_salesforce_payload)
    teams = [Team(name="Team US", region="US", engineers=[engineer])]
    with pytest.raises(NoAvailableEngineerError) as exc_info:
        routing_strategy.route(ticket, teams)
    assert (
        str(exc_info.value)
        == f"No available engineer for ticket {ticket.ticket_id!r}: "
        "No engineers currently on shift"
    )
