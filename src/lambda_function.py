from loguru import logger

from views.telegram_view import TelegramView

telegram_view = TelegramView()


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    logger.info(f"Received context: {context}")

    return telegram_view.awnser_message(event)
