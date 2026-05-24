from celonis_support_utils.repository import InMemoryTicketRepository


def test_InMemoryTicketRepository_save_get_by_id(sample_salesforce_ticket):
    repo = InMemoryTicketRepository()
    repo.save(sample_salesforce_ticket)
    assert (
        repo.get_by_id(sample_salesforce_ticket.ticket_id) == sample_salesforce_ticket
    )


def test_InMemoryTicketRepository_list_open(sample_salesforce_ticket):
    repo = InMemoryTicketRepository()
    repo.save(sample_salesforce_ticket)
    open_tickets = repo.list_open()
    assert len(open_tickets) == 1
    assert open_tickets[0] == sample_salesforce_ticket


def test_InMemoryTicketRepository_unknown_ticket_id(sample_salesforce_ticket):
    repo = InMemoryTicketRepository()
    repo.save(sample_salesforce_ticket)
    assert repo.get_by_id("unknown_id") is None
