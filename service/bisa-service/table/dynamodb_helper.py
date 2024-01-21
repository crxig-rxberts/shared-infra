from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from app_config import AppConfig


class DynamoDBHelper:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.table = self.dynamodb.Table(AppConfig.DYNAMO_TABLE_NAME)

    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item', None)
        except ClientError as e:
            print(f"Failed to get item: {e.response['Error']['Message']}")
            return None

    def update_item(self, key, update_expression, expression_attribute_values):
        try:
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return True
        except ClientError as e:
            print(f"Failed to update item: {e.response['Error']['Message']}")
            return False

    def get_item_by_card_number(self, card_number):
        try:
            response = self.table.query(
                IndexName='CardNumberIndex',
                KeyConditionExpression=Key('cardNumber').eq(card_number)
            )
            items = response.get('Items', [])
            if items:
                return items[0]
            return None
        except ClientError as e:
            print(f"Failed to query item: {e.response['Error']['Message']}")
            return None
