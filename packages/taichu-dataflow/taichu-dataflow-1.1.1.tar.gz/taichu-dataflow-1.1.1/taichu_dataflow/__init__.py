import json
from datetime import datetime
import logging
import os
import sys
import threading
import requests


class AsyncHttpPostHandler(logging.Handler):
    def __init__(self, url, **kwargs):
        logging.Handler.__init__(self)
        self.url = url

    def emit(self, record):
        log_entry = self.format(record)
        thread = threading.Thread(target=self._send_log_entry, args=(log_entry,))
        thread.start()

    def _send_log_entry(self, log_entry):
        try:
            json_data = json.loads(log_entry)
            response = requests.post(self.url, json=json_data)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send log entry: {repr(e)}")


log_collector_url = 'http://58.48.42.242:8088/log/collector'


def init_logger(url):
    log_dir = f'/tmp/dataflow/'
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'{log_dir}{datetime.now().strftime("%Y-%m-%d")}.log', mode="a")
        ],
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s'
    )
    handler = AsyncHttpPostHandler(url=url)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


init_logger(log_collector_url)
