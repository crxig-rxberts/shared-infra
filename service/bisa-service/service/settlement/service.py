from decimal import Decimal
from service.response import Response


class SettlementService:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def settle(self, card_number, amount):
        card_info = self.db_helper.get_item_by_card_number(card_number)
        if not card_info:
            return Response.failure("Card not found")

        if not self._has_sufficient_balance(card_info, amount):
            return Response.failure("Insufficient funds")

        return self._update_balance(card_info, amount)

    @staticmethod
    def _has_sufficient_balance(card_info, amount):
        if 'balance' not in card_info:
            return False

        current_balance = Decimal(card_info['balance'])
        return current_balance >= Decimal(amount)

    def _update_balance(self, card_info, amount):
        new_balance = Decimal(card_info['balance']) - Decimal(amount)
        key = {'id': card_info['id']}
        update_expression = "set balance = :b"
        expression_attribute_values = {':b': new_balance}

        if self.db_helper.update_item(key, update_expression, expression_attribute_values):
            return Response.success("Settlement completed")
        else:
            return Response.failure("Failed to update balance")

