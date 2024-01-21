import rpyc

from table.transaction_persistence import TransactionPersistence
from service.bisa.authenticate import AuthenticationService
from service.bisa.authorise import AuthorisationService
from service.bisa.bisa_client import BisaClient
import uuid
import logging

from service.bisa.settle import SettlementService


class PaymentService(rpyc.Service):
    def __init__(self, dynamodb):
        self.logger = logging.getLogger(__name__)
        self.bisa = BisaClient().get_service()
        self.auth_service = AuthenticationService(self.bisa)
        self.authorisation_service = AuthorisationService(self.bisa)
        self.settlement_service = SettlementService(self.bisa)
        self.transaction_persistence = TransactionPersistence(dynamodb)

    def exposed_processor(self, transaction_request):
        transaction_id = str(uuid.uuid4())

        if not self.bisa:
            return self.handle_downstream_error(transaction_id, transaction_request)

        auth_response = self.auth_service.authenticate(transaction_request)
        if auth_response['status'] == 'failure':
            return self.finalise_transaction(transaction_id, transaction_request, auth_response)

        authorise_response = self.authorisation_service.authorise(transaction_request)
        if authorise_response['status'] == 'failure':
            return self.finalise_transaction(transaction_id, transaction_request, auth_response, authorise_response)

        settle_response = self.settlement_service.settle(transaction_request)
        return self.finalise_transaction(transaction_id, transaction_request, auth_response, authorise_response, settle_response)

    def handle_downstream_error(self, transaction_id, transaction_request):
        self.logger.error("Failed to connect to Bisa service")
        return {
            'id': transaction_id,
            'status': 'FAILURE',
            'message': 'Failure connecting to downstream payment providers.',
            'CardNum': '************' + transaction_request['card_num'][-4:],
            'Amount': transaction_request['amount'],
        }

    def finalise_transaction(self, transaction_id, transaction_request, auth_response, authorise_response=None, settle_response=None):
        self.transaction_persistence.save_transaction(transaction_id, transaction_request, auth_response, authorise_response, settle_response)

        return self.prepare_response(
            transaction_id, transaction_request, auth_response, authorise_response, settle_response,
            'SUCCESS' if settle_response and settle_response['status'] == 'success' else 'FAILURE'
        )

    @staticmethod
    def prepare_response(transaction_id, request, auth_response=None, authorise_response=None, settle_response=None, status='FAILURE'):
        response = {
            'id': transaction_id,
            'status': status,
            'CardNum': '************' + request['card_num'][-4:],
            'Amount': request['amount'],
        }
        if auth_response:
            response['authentication'] = auth_response
        if authorise_response:
            response['authorisation'] = authorise_response
        if settle_response:
            response['settlement'] = settle_response
        return response
