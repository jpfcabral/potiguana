from typing import Any, Dict

import boto3
from boto3.dynamodb.types import TypeSerializer
from loguru import logger

serializer = TypeSerializer()


class DynamoDBRepository:
    def __init__(self, client: Any = None):
        """"""
        if not client:
            client = boto3.client("dynamodb", region_name="us-east-1")

        self.client = client

    def insert(self, data: Dict[str, Any], table_name: str):
        """"""
        try:
            item_serialized = {k: serializer.serialize(v) for k, v in data.items()}
            return self.client.put_item(TableName=table_name, Item=item_serialized)
        except Exception as exc:
            logger.error(f"Error to insert data in database: {exc}")
            return None
