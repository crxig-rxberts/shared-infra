import os


class AppConfig:
    DYNAMO_ENDPOINT_URL = os.getenv('DYNAMO_ENDPOINT_URL', 'http://localhost:8000')
    DYNAMO_REGION_NAME = 'eu-west-1'
    DYNAMO_TABLE_NAME = 'payments'

    BISA_HOST_IP = '54.228.89.136'
    BISA_HOST_PORT = 18080
    BISA_MAX_RETRIES = 1
    BISA_RETRY_INTERVAL = 1
    BISA_VALID_CARD_BINS = {"8002"}
