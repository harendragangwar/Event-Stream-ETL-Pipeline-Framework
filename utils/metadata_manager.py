import os
import json
from datetime import datetime
class PipelineMetadataTracker:
    def __init__(self, logger):
        self.logger = logger
    def generate_run_summary(self, execution_id, total, clean, meta_dir="data/metadata"):
        summary = {
            "run_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "total_extracted": total,
            "total_processed": clean,
            "dropped_records": total - clean,
            "status": "SUCCESS"
        }
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)
        target_path = f"{meta_dir}/summary_{execution_id}.json"
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        self.logger.info("Metadata logs flushed securely to target destination checkpoint")
