import logging

import rpyc
import time
from app_config import AppConfig

logger = logging.getLogger(__name__)


class BisaClient:
    def __init__(self):
        self.host = AppConfig.BISA_HOST_IP
        self.port = AppConfig.BISA_HOST_PORT
        self.max_retries = AppConfig.BISA_MAX_RETRIES
        self.retry_interval = AppConfig.BISA_RETRY_INTERVAL

    def connect(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                return rpyc.connect(self.host, self.port)
            except Exception as e:
                retry_count += 1
                logger.warning(f"Attempt {retry_count} failed: Error connecting to Bisa service: {e}")
                if retry_count < self.max_retries:
                    time.sleep(self.retry_interval)
                else:
                    logger.error(f"Failed to connect to Bisa service after multiple attempts. ex: {e}")

    def get_service(self):
        bisa_conn = self.connect()
        if bisa_conn:
            return bisa_conn.root
        else:
            return None
