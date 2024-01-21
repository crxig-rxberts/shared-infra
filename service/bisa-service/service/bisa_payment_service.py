from rpyc import Service
from table.dynamodb_helper import DynamoDBHelper
from .authentication.service import AuthenticationService
from .authorisation.service import AuthorisationService
from .response import Response
from .settlement.service import SettlementService


class BisaPaymentService(Service):
    def __init__(self, dynamodb):
        self.db_helper = DynamoDBHelper(dynamodb)
        self.auth_service = AuthenticationService(self.db_helper)
        self.authorisation_service = AuthorisationService(self.db_helper)
        self.settlement_service = SettlementService(self.db_helper)

    exposed_Response = Response

    def exposed_authenticate_transaction(self, card_number, cvv, expiry_date):
        return self.auth_service.authenticate(card_number, cvv, expiry_date).to_dict()

    def exposed_authorise_transaction(self, card_number, amount):
        return self.authorisation_service.authorise(card_number, amount).to_dict()

    def exposed_settle_transaction(self, card_number, amount):
        return self.settlement_service.settle(card_number, amount).to_dict()
