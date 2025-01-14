from typing import Any

import requests

from config.settings import settings
from repositories.dynamodb_repository import DynamoDBRepository


class TelegramService:
    def __init__(
        self,
        api_token: str = settings.TELEGRAM_API_TOKEN,
        repository: DynamoDBRepository = DynamoDBRepository(),
    ):
        self._api_token = api_token
        self.repository = repository

    def send_message(self, body: dict, message: str):
        chat_id = body["message"]["chat"]["id"]

        url = f"https://api.telegram.org/bot{self._api_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message + "\n\n Essa resposta foi útil?",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "Sim", "callback_data": "sim"},
                        {"text": "Não", "callback_data": "nao"},
                    ]
                ]
            },
        }

        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()

        body["response"] = payload
        self.repository.insert(data=body, table_name="messages")

        return response.json()

    def save_callback(self, body: dict):
        """"""
        return self.repository.insert(data=body, table_name="callback")
