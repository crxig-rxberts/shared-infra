import os


class AppConfig:
    DYNAMO_ENDPOINT_URL = os.getenv('DYNAMO_ENDPOINT_URL', 'http://localhost:8000')
    DYNAMO_REGION_NAME = 'eu-west-1'
    DYNAMO_TABLE_NAME = 'card-table'

