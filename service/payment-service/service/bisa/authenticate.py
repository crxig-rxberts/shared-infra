from app_config import AppConfig


class AuthenticationService:
    def __init__(self, bisa):
        self.bisa = bisa

    def authenticate(self, transaction_request):
        for valid_bin in AppConfig.BISA_VALID_CARD_BINS:

            if transaction_request['card_num'].startswith(valid_bin):
                return self.bisa.authenticate_transaction(
                    transaction_request['card_num'],
                    transaction_request['cvv'],
                    transaction_request['expiry']
                )
            else:
                return {'status': 'failure', 'message': 'Bad Request: Not a valid BISA card'}
