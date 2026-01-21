import os
import json
from datetime import datetime
class PipelineMetadataTracker:
    def __init__(self, logger):
        self.logger = logger
    def generate_run_summary(self, execution_id, total, clean):
        summary = {
            "run_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "total_extracted": total,
            "total_processed": clean,
            "dropped_records": total - clean,
            "status": "SUCCESS"
        }
        meta_dir = "data/metadata"
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)
        with open(f"{meta_dir}/summary_{execution_id}.json", "w") as f:
            json.dump(summary, f, indent=2)
        self.logger.info("Pipeline run summary metadata saved successfully")
