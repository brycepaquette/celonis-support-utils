from celonis_support_utils.ticket import TicketStatus


def test_save_get_by_id(sample_salesforce_ticket, repo):
    repo.save(sample_salesforce_ticket)
    assert (
        repo.get_by_id(sample_salesforce_ticket.ticket_id) == sample_salesforce_ticket
    )


def test_list_open(sample_salesforce_ticket, repo):
    repo.save(sample_salesforce_ticket)
    open_tickets = repo.list_open()
    assert len(open_tickets) == 1
    assert open_tickets[0] == sample_salesforce_ticket


def test_unknown_ticket_id(sample_salesforce_ticket, repo):
    repo.save(sample_salesforce_ticket)
    assert repo.get_by_id("unknown_id") is None


def test_list_open_excludes_closed(sample_salesforce_ticket, repo):
    sample_salesforce_ticket.status = TicketStatus.CLOSED
    repo.save(sample_salesforce_ticket)
    assert repo.list_open() == []
