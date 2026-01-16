import os
import sys
import json
import random
from datetime import datetime
from utils.logger import setup_production_logging

class DataPipelineCore:
    def __init__(self):
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.status = "INITIALIZED"
        self.logger = setup_production_logging()
        self._load_config()
        self.logger.info(f"Pipeline Run ID {self.execution_id} launched successfully")

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
                "action": random.choice(events) if random.random() > 0.1 else None,
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

    def validate_records(self, data):
        clean_data = []
        for record in data:
            if not record.get("action") or not record.get("event_id"):
                self.logger.warning(f"Skipping bad record missing critical fields: {record['event_id']}")
                continue
            clean_data.append(record)
        self.logger.info(f"Validation complete. Passed: {len(clean_data)}/{len(data)}")
        return clean_data

    def transform_payload(self, data):
        transformed = []
        for record in data:
            payload = record.copy()
            payload["action"] = str(payload["action"]).upper()
            payload["processed_at"] = datetime.now().isoformat()
            payload["source_system"] = "web_store_front"
            transformed.append(payload)
        self.logger.info(f"Transformation node applied formatting to {len(transformed)} nodes")
        return transformed

    def load_processed_data(self, data):
        proc_dir = "data/processed"
        if not os.path.exists(proc_dir):
            os.makedirs(proc_dir)
        file_path = f"{proc_dir}/clean_events_{self.execution_id}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Successfully loaded transformed batch into destination sink: {file_path}")

    def generate_run_summary(self, total, clean):
        summary = {
            "run_id": self.execution_id,
            "timestamp": datetime.now().isoformat(),
            "total_extracted": total,
            "total_processed": clean,
            "dropped_records": total - clean,
            "status": "SUCCESS"
        }
        meta_dir = "data/metadata"
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)
        with open(f"{meta_dir}/summary_{self.execution_id}.json", "w") as f:
            json.dump(summary, f, indent=2)
        self.logger.info("Pipeline run summary metadata saved successfully")

    def run_pipeline(self):
        self.logger.info("Executing active data node checkpoints")
        self.status = "RUNNING"
        raw_data = self.extract_raw_logs()
        self.save_raw_data(raw_data)
        validated_data = self.validate_records(raw_data)
        transformed_data = self.transform_payload(validated_data)
        self.load_processed_data(transformed_data)
        self.generate_run_summary(len(raw_data), len(transformed_data))
        return True

if __name__ == "__main__":
    engine = DataPipelineCore()
    engine.run_pipeline()
