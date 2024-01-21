from decimal import Decimal
from service.response import Response


class AuthorisationService:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def authorise(self, card_number, amount):
        card_info = self.db_helper.get_item_by_card_number(card_number)
        if not card_info:
            return Response.failure("Card not found.")

        return self.verify_balance(card_info, amount)

    @staticmethod
    def verify_balance(card_info, amount):
        if 'balance' not in card_info:
            return Response.failure("Balance information not found")

        current_balance = Decimal(card_info['balance'])
        amount = Decimal(amount)

        if current_balance < amount:
            return Response.failure("Transaction declined. Insufficient balance.")

        return Response.success("Authorisation successful")
