from typing import Any

import requests
from loguru import logger

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

    def send_message(
        self,
        body: dict,
        message: str,
        ask_feedback: bool = False,
        add_suggestions: bool = False,
    ):
        payload = dict()
        chat_id = body["message"]["chat"]["id"]

        url = f"https://api.telegram.org/bot{self._api_token}/sendMessage"

        payload["chat_id"] = chat_id
        payload["text"] = message

        if ask_feedback:
            payload["text"] = payload["text"] + "\n\n Essa resposta foi útil?"
            payload["reply_markup"] = self._get_inline_keyboard()

        if add_suggestions:
            payload["reply_markup"] = self._get_reply_keyboard_markup()

        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()

        body["response"] = payload
        self.repository.insert(data=body, table_name="messages")

        return response.json()

    def _get_inline_keyboard(self):
        data = dict()
        data["inline_keyboard"] = [
            [
                {"text": "Sim", "callback_data": "sim"},
                {"text": "Não", "callback_data": "nao"},
            ]
        ]

        return data

    def _get_reply_keyboard_markup(self):
        data = dict()

        data["keyboard"] = [
            [
                {"text": "Quando começam as aulas?"},
                {"text": "O que preciso fazer para cancelar o curso?"},
            ]
        ]

        data["resize_keyboard"] = True
        data["one_time_keyboard"] = True

        return data

    def save_callback(self, body: dict):
        """"""
        return self.repository.insert(data=body, table_name="callbacks")

    def answer_callback_query(self, id: str):
        payload = dict()

        payload["callback_query_id"] = id

        url = f"https://api.telegram.org/bot{self._api_token}/answerCallbackQuery"

        response = requests.post(url=url, json=payload, timeout=15)
        response.raise_for_status()

        return response.json()
