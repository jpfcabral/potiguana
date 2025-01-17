import json
import traceback

from loguru import logger

from services.chatbot_service import ChatbotService
from services.telegram_service import TelegramService


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    logger.info(f"Received context: {context}")

    chatbot = ChatbotService()
    telegram_service = TelegramService()

    try:
        body = json.loads(event["body"])

        if "message" in body:
            message_part = body["message"].get("text")

            response = chatbot.answer(query=message_part)
            telegram_service.send_message(
                body=body,
                message=response["content"],
                ask_feedback=True if "route" not in response else False,
                add_suggestions=True
                if response.get("route", None) == "greetings"
                else False,
            )

            return {"statusCode": 200}

        if "callback_query" in body:
            callback_id = body["callback_query"]["id"]
            telegram_service.answer_callback_query(id=callback_id)
            telegram_service.save_callback(body=body)

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
