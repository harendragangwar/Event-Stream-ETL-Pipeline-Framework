import os
import time
import shutil
from datetime import datetime, timedelta

class PipelineAutoCleanupEngine:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.raw_dir = config.get("raw_stage_path", "data/raw")
        self.processed_dir = config.get("processed_stage_path", "data/processed")
        self.retention_hours = config.get("max_staging_directory_retention_hours", 24)

    def execute_retention_purge(self):
        self.logger.info(f"Starting automated staging cleanup engine. Threshold policy: {self.retention_hours} Hours")
        purged_count = 0
        cutoff_time = time.time() - (self.retention_hours * 3600)
        
        target_dirs = [self.raw_dir, self.processed_dir]
        for folder in target_dirs:
            if not os.path.exists(folder):
                continue
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.unlink(file_path)
                            purged_count += 1
                    elif os.path.isdir(file_path):
                        if os.path.getmtime(file_path) < cutoff_time:
                            shutil.rmtree(file_path)
                            purged_count += 1
                except Exception as e:
                    self.logger.warning(f"Unable to purge staging artifact index {file_path}: {str(e)}")
                    
        self.logger.info(f"Purge complete. Safely removed {purged_count} stale transient files | State: SUCCESS")
        return purged_count
