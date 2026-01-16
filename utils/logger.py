import os
import sys
import logging

def setup_production_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_format = "%(asctime)s [%(levelname)s] - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f"{log_dir}/pipeline_execution.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("EnterprisePipeline")
