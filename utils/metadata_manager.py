import os
import json
from datetime import datetime

class PipelineMetadataTracker:
    def __init__(self, logger):
        self.logger = logger

    def generate_run_summary(self, execution_id, total, clean, meta_dir="data/metadata"):
        dropped = total - clean
        efficiency_rate = round((clean / total) * 100, 2) if total > 0 else 100.0
        
        summary = {
            "run_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_extracted": total,
                "total_processed": clean,
                "dropped_records": dropped,
                "pipeline_efficiency_pct": efficiency_rate
            },
            "environment_telemetry": {
                "engine_version": "1.3.5",
                "system_status": "HEALTHY" if dropped / (total if total > 0 else 1) < 0.3 else "DEGRADED"
            }
        }
        
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)
            
        target_path = f"{meta_dir}/summary_{execution_id}.json"
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            
        self.logger.info(f"Detailed metadata run report flushed to storage. Efficiency: {efficiency_rate}%")
        return summary
