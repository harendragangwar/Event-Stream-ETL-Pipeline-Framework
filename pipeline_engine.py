import os
import sys
import json
import logging
import random
from datetime import datetime

class DataPipelineCore:
    def __init__(self):
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.status = "INITIALIZED"
        self._setup_production_logging()
        self._load_config()
        self.logger.info(f"Pipeline Run ID {self.execution_id} launched successfully")

    def _setup_production_logging(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_format = "%(asctime)s [%(levelname)s] - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[logging.FileHandler(f"{log_dir}/pipeline_execution.log"), logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger("EnterprisePipeline")

    def _load_config(self):
        self.config = {"batch_size": 500, "retry_limit": 3, "timeout": 30}
        self.logger.info("Basic pipeline configuration dictionary loaded")

    def extract_raw_logs(self):
        self.logger.info("Starting mock data extraction from source endpoint")
        events = ["click", "view", "purchase", "cart_add"]
        mock_data = []
        for i in range(10):
            record = {
                "event_id": f"evt_{random.randint(1000, 9999)}",
                "timestamp": datetime.now().isoformat(),
                "action": random.choice(events),
                "user_id": f"usr_{random.randint(1, 100)}"
            }
            mock_data.append(record)
        self.logger.info(f"Successfully extracted {len(mock_data)} raw event logs")
        return mock_data

    def save_raw_data(self, data):
        raw_dir = "data/raw"
        if not os.path.exists(raw_dir):
            os.makedirs(raw_dir)
        file_path = f"{raw_dir}/raw_events_{self.execution_id}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Saved raw extraction batch to local path: {file_path}")

    def run_pipeline(self):
        self.logger.info("Executing active data node checkpoints")
        self.status = "RUNNING"
        data = self.extract_raw_logs()
        self.save_raw_data(data)
        return True

if __name__ == "__main__":
    engine = DataPipelineCore()
    engine.run_pipeline()
