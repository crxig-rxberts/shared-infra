import uuid
from decimal import Decimal

import boto3

from app_config import AppConfig


def initialize_card_table_with_data(table):
    test_cards = [
        {"cardNumber": "8002 1235 5687 9898", "expiryDate": "12/24", "cvv": "994", "balance": Decimal('98.99')},
        {"cardNumber": "8002 6543 3456 7634", "expiryDate": "02/23", "cvv": "456", "balance": Decimal('101.00')},
        {"cardNumber": "8002 8945 2356 8345", "expiryDate": "02/25", "cvv": "546", "balance": Decimal('56.00')},
        {"cardNumber": "8002 6354 2345 8765", "expiryDate": "06/26", "cvv": "134", "balance": Decimal('23.00')}
    ]

    for card in test_cards:
        card['id'] = str(uuid.uuid4())
        table.put_item(Item=card)


def configure_dynamodb():
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=AppConfig.DYNAMO_ENDPOINT_URL,
            region_name=AppConfig.DYNAMO_REGION_NAME
        )

        if "localhost" not in AppConfig.DYNAMO_ENDPOINT_URL:
            initialize_card_table_with_data(dynamodb.Table(AppConfig.DYNAMO_TABLE_NAME))

        return dynamodb

    except Exception as e:
        print(f"Error configuring DynamoDB: {e}")
        exit(1)
