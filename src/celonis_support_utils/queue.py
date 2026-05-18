from celonis_support_utils.ticket import Ticket


class Queue:
    def __init__(self, name: str):
        self.name = name
        self._queue: list[Ticket] = []

    def add(self, ticket: Ticket) -> None:
        self._queue.append(ticket)

    def next(self) -> Ticket | None:
        if not self._queue:
            return None
        return self._queue.pop(0)
