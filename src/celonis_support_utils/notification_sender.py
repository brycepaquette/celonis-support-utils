from abc import ABC, abstractmethod

import requests


class NotificationSender(ABC):
    """Abstract base class for sending notifications."""

    @abstractmethod
    def send(self, message: str) -> None: ...


class SlackSender(NotificationSender):
    """Concrete implementation of NotificationSender for sending messages to Slack."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str) -> None:
        """Sends a message to a Slack channel using the provided webhook URL."""
        payload = {"text": message}
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()
