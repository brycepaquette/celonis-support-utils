from abc import ABC, abstractmethod

import requests


class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class SlackSender(NotificationSender):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str) -> None:
        payload = {"text": message}
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()
