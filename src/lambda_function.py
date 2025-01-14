import json
import traceback

import requests
from loguru import logger

from config.settings import settings
from services.chatbot_service import ChatbotService
from services.telegram_service import TelegramService


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    logger.info(f"Received context: {context}")
    try:
        body = json.loads(event["body"])

        if "message" in body:
            chat_id = body["message"]["chat"]["id"]
            message_part = body["message"].get("text")

            chatbot = ChatbotService()
            telegram_service = TelegramService()

            response = chatbot.answer(query=message_part)
            telegram_service.send_message(chat_id=chat_id, message=response["content"])

            return {"statusCode": 200}

        raise Exception(f"Unknown request: {body}")
    except Exception as exc:
        logger.error(exc)
        logger.error(f"Detalhes do traceback:\n {traceback.format_exc()}")
        return {
            "statusCode": 200,
            "error": str(exc),
            "text": "Erro",
        }
