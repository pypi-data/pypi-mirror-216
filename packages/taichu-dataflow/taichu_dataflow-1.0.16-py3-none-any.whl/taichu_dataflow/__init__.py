import logging
import os
import sys
import threading


def init_filebeat():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'filebeat.sh')
    os.system(f"/bin/bash {script_path} >/dev/null 2>&1")


def init_logger():
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("/tmp/dataflow.log", mode="a")
        ],
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s'
    )


# threading.Thread(target=init_filebeat).start()
init_logger()
