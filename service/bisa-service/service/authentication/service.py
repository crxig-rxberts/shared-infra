from datetime import datetime
from service.response import Response


class AuthenticationService:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def authenticate(self, card_number, cvv, expiry_date):
        card_info = self.db_helper.get_item_by_card_number(card_number)
        if not card_info:
            return Response.failure("Card not found")

        if not self._validate_cvv(card_info, cvv):
            return Response.failure("Transaction declined. CVV incorrect.")

        if not self._validate_expiry_dates(card_info, expiry_date):
            return Response.failure("Transaction declined. Expiry date does not match.")

        if self._is_card_expired(card_info):
            return Response.failure("Transaction declined. Card expired.")

        return Response.success("Authentication successful")

    @staticmethod
    def _validate_cvv(card_info, cvv):
        return card_info.get('cvv') == cvv

    @staticmethod
    def _validate_expiry_dates(card_info, expiry_date):
        stored_expiry_date = datetime.strptime(card_info.get('expiryDate'), "%m/%y")
        provided_expiry_date = datetime.strptime(expiry_date, "%m/%y")
        return provided_expiry_date == stored_expiry_date

    @staticmethod
    def _is_card_expired(card_info):
        stored_expiry_date = datetime.strptime(card_info.get('expiryDate'), "%m/%y")
        return stored_expiry_date < datetime.now()
