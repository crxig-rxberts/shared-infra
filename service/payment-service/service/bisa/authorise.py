class AuthorisationService:
    def __init__(self, bisa):
        self.bisa = bisa

    def authorise(self, transaction_request):
        return self.bisa.authorise_transaction(
            transaction_request['card_num'],
            transaction_request['amount']
        )
