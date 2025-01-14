import requests

from config.settings import settings


class TelegramService:
    def __init__(self, api_token: str = settings.TELEGRAM_API_TOKEN):
        self._api_token = api_token

    def send_message(self, chat_id: int, message: str):
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

        return response.json()
