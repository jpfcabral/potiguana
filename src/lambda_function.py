import json

import requests
from loguru import logger

from config.settings import settings
from services.chatbot_service import ChatbotService


def lambda_handler(event, context):
    try:
        logger.info("Init telegram request")
        chatbot = ChatbotService()
        body = json.loads(event["body"])
        chat_id = body["message"]["chat"]["id"]

        logger.info(f"Message body: {body}")

        message_part = body["message"].get("text")
        print("Message part : {}".format(message_part))

        response = chatbot.answer(query=message_part)

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": response["content"]}

        r = requests.post(url, json=payload, timeout=10)

        return {"statusCode": 200}
    except Exception as exc:
        logger.error(exc)
        return {
            "statusCode": 500,
            "error": str(exc),
            "chat_id": chat_id,
            "text": "Erro",
        }
