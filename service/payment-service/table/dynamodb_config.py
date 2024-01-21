import boto3

from app_config import AppConfig


def configure_dynamodb():
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=AppConfig.DYNAMO_ENDPOINT_URL,
            region_name=AppConfig.DYNAMO_REGION_NAME
        )

        return dynamodb

    except Exception as e:
        print(f"Error configuring DynamoDB: {e}")
        exit(1)
