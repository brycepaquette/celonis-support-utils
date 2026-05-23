class Queue[T]:
    """FIFO queue for ordered item processing."""

    def __init__(self, name: str):
        if not name:
            raise ValueError("Queue name cannot be empty.")
        self.name = name
        self._queue: list[T] = []

    def add(self, item: T) -> None:
        """Add an item to the end of the queue."""
        self._queue.append(item)

    def next(self) -> T | None:
        """Remove and return the next item, or None if empty."""
        if not self._queue:
            return None
        return self._queue.pop(0)

    def __len__(self) -> int:
        return len(self._queue)

    def __bool__(self) -> bool:
        return bool(self._queue)
