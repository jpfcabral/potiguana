import json
import traceback

import requests
from loguru import logger

from config.settings import settings
from services.chatbot_service import ChatbotService


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    logger.info(f"Received context: {context}")

    try:
        logger.info(f"Init telegram request with: {event}")
        chatbot = ChatbotService()
        body = json.loads(event["body"])
        chat_id = body["message"]["chat"]["id"]

        logger.info(f"Message body: {body}")

        message_part = body["message"].get("text")
        print("Message part : {}".format(message_part))

        response = chatbot.answer(query=message_part)

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": response["content"] + "\n\n Essa resposta foi útil?",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "Sim", "callback_data": "sim"},
                        {"text": "Não", "callback_data": "nao"},
                    ]
                ]
            },
        }

        r = requests.post(url, json=payload, timeout=10)

        return {"statusCode": 200}
    except Exception as exc:
        logger.error(exc)
        logger.error(f"Detalhes do traceback:\n {traceback.format_exc()}")
        return {
            "statusCode": 200,
            "error": str(exc),
            "text": "Erro",
        }
