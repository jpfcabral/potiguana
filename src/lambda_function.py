import json

import requests

from config.settings import settings


def lambda_handler(event, context):
    print(event)
    try:
        body = json.loads(event["body"])

        print(body)

        message_part = body["message"].get("text")
        print("Message part : {}".format(message_part))

        chat_id = body["message"]["chat"]["id"]

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": "hello"}

        r = requests.post(url, json=payload, timeout=10)

        return {"statusCode": 200}
    except:
        return {"statusCode": 500}
