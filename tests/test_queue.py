import pytest

from celonis_support_utils.queue import Queue
from celonis_support_utils.ticket import Ticket


@pytest.fixture
def queue():
    return Queue(
        name="Test Queue",
    )


def test_queue_name_empty():
    with pytest.raises(ValueError) as exc_info:
        Queue(name="")
    assert "Queue name cannot be empty" in str(exc_info.value)


def test_queue_add(queue, sample_salesforce_ticket_payload):
    new_ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    queue.add(new_ticket)
    assert len(queue._queue) == 1
    assert queue._queue[0] == new_ticket


def test_queue_next(queue, sample_salesforce_ticket_payload):
    new_ticket = Ticket.from_salesforce_payload(sample_salesforce_ticket_payload)
    queue.add(new_ticket)
    next_ticket = queue.next()
    assert next_ticket == new_ticket
    assert len(queue._queue) == 0
