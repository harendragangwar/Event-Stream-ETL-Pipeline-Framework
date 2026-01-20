import os
import json

class DiskDataLoader:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def save_raw_data(self, data, execution_id):
        raw_dir = self.config["raw_stage_path"]
        if not os.path.exists(raw_dir):
            os.makedirs(raw_dir)
        file_path = f"{raw_dir}/raw_events_{execution_id}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Saved raw extraction batch to local path: {file_path}")

    def load_processed_data(self, data, execution_id):
        proc_dir = self.config["processed_stage_path"]
        if not os.path.exists(proc_dir):
            os.makedirs(proc_dir)
        file_path = f"{proc_dir}/clean_events_{execution_id}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Successfully loaded transformed batch into destination sink: {file_path}")
