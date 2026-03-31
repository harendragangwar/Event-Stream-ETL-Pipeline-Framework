import os
import json
from utils.exceptions import StorageLoadError

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
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise StorageLoadError(f"Failed writing load records to target stage path: {str(e)}")
        self.logger.info(f"Successfully loaded transformed batch into destination sink: {file_path}")

    def verify_load_sync(self, execution_id):
        proc_dir = self.config["processed_stage_path"]
        target = f"{proc_dir}/clean_events_{execution_id}.json"
        status = os.path.exists(target) and os.path.getsize(target) > 0
        if status:
            file_size_kb = os.path.getsize(target) / 1024
            self.logger.info(f"Storage load verification clear. Node size: {file_size_kb:.2f} KB")
        else:
            self.logger.error(f"Downstream transaction check mismatch for execution node: {execution_id}")
        return status
