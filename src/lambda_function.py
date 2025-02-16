import json
import traceback

from loguru import logger

from config.texts import GREETING
from services.chatbot_service import ChatbotService
from services.telegram_service import TelegramService

chatbot = ChatbotService()
telegram_service = TelegramService()


def answer_message(body: dict):
    message_part = body["message"].get("text")

    if message_part == "/start":
        telegram_service.send_message(body=body, message=GREETING, add_suggestions=True)
        return {"statusCode": 200}

    response = chatbot.answer(query=message_part)
    telegram_service.send_message(
        body=body,
        message=response["content"],
        ask_feedback=True if "route" not in response else False,
        add_suggestions=True if response.get("route", None) == "greetings" else False,
    )

    return {"statusCode": 200}


def answer_callback_query(body: dict):
    callback_id = body["callback_query"]["id"]
    telegram_service.answer_callback_query(id=callback_id)
    telegram_service.save_callback(body=body)

    return {"statusCode": 200}


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    logger.info(f"Received context: {context}")

    try:
        body = json.loads(event["body"])

        if "message" in body:
            return answer_message(body=body)

        if "callback_query" in body:
            return answer_callback_query(body=body)

        raise Exception(f"Unknown request: {body}")
    except Exception as exc:
        logger.error(exc)
        logger.error(f"Detalhes do traceback:\n {traceback.format_exc()}")
        return {
            "statusCode": 200,
            "error": str(exc),
            "text": "Erro",
        }
