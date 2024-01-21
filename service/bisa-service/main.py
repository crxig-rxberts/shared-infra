import logging

from rpyc.utils.server import ThreadedServer
from table.dynamodb_config import configure_dynamodb
from service.bisa_payment_service import BisaPaymentService


def init_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    return logging.getLogger(__name__)


if __name__ == '__main__':
    logger = init_logger()
    dynamodb = configure_dynamodb()
    service = BisaPaymentService(dynamodb)
    server = ThreadedServer(service, port=18080, protocol_config={"allow_pickle": True})

    logger.info('BISA Payment Service starting on port 18080...')
    server.start()
