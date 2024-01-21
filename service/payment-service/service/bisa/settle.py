class SettlementService:
    def __init__(self, bisa):
        self.bisa = bisa

    def settle(self, transaction_request):
        return self.bisa.settle_transaction(
            transaction_request['card_num'],
            transaction_request['amount']
        )
