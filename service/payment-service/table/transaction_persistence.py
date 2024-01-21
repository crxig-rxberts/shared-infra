import logging
from decimal import Decimal
import json

from app_config import AppConfig


class TransactionPersistence:
    def __init__(self, dynamodb):
        self.logger = logging.getLogger(__name__)
        self.payments_table = dynamodb.Table(AppConfig.DYNAMO_TABLE_NAME)

    def save_transaction(self, transaction_id, request, auth_response, authorise_response, settle_response):
        self.handle_decimal_type_conversion(request, settle_response)

        try:
            self.payments_table.put_item(Item={

                'id': transaction_id,
                'request': {
                    'CardNum': '************' + request['card_num'][-4:],
                    'Expiry': request['expiry'],
                    'Amount': request['amount']
                },
                'authentication': self.ensure_serializable(auth_response),
                'authorisation': self.ensure_serializable(authorise_response),
                'settlement': self.ensure_serializable(settle_response)
            })

            self.logger.info("Transaction saved successfully.")

        except Exception:
            self.logger.exception("Error saving transaction: ", exc_info=True)

    @staticmethod
    def handle_decimal_type_conversion(request, settle_response):
        request['amount'] = Decimal(str(request['amount']))
        if settle_response and 'amount' in settle_response:
            settle_response['amount'] = Decimal(str(settle_response['amount']))

    @staticmethod
    def ensure_serializable(response):
        try:
            json.dumps(response)
            return response
        except TypeError:
            return str(response)
