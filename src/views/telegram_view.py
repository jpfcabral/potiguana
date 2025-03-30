import json
import traceback

from loguru import logger

from config.texts import GREETING
from services.chatbot_service import ChatbotService
from services.telegram_service import TelegramService

chatbot = ChatbotService()
telegram_service = TelegramService()


class TelegramView:
    def answer_message(self, event):
        try:
            body = json.loads(event["body"])

            if "message" in body:
                return self._answer_message(body=body)

            if "callback_query" in body:
                return self._answer_callback_query(body=body)

            raise Exception(f"Unknown request: {body}")
        except Exception as exc:
            logger.error(exc)
            logger.error(f"Detalhes do traceback:\n {traceback.format_exc()}")
            return {
                "statusCode": 200,
                "error": str(exc),
                "text": "Erro",
            }

    def _answer_message(self, body: dict):
        message_part = body["message"].get("text")
        chat_id = body["message"]["chat"]["id"]

        if message_part == "/start":
            return self._greeting(body=body)

        response = chatbot.answer(query=message_part, chat_id=chat_id)
        telegram_service.send_message(
            body=body,
            message=response["content"],
            ask_feedback=True if "route" not in response else False,
            add_suggestions=(
                True if response.get("route", None) == "greetings" else False
            ),
        )

        return {"statusCode": 200}

    def _answer_callback_query(self, body: dict):
        callback_id = body["callback_query"]["id"]
        telegram_service.answer_callback_query(id=callback_id)
        telegram_service.save_callback(body=body)

        return {"statusCode": 200}

    def _greeting(self, body: dict):
        telegram_service.send_message(body=body, message=GREETING, add_suggestions=True)
        return {"statusCode": 200}
