import os
import sys

class PipelineSystemMonitor:
    def __init__(self, logger):
        self.logger = logger

    def collect_memory_usage(self):
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
            self.logger.info(f"System memory tracking verification metric: {mem_mb:.2f} MB")
            return mem_mb
        except Exception:
            self.logger.warning("Native process telemetry profiling metrics missing or offline")
            return 0.0

    def check_disk_space(self, target_path="."):
        try:
            import shutil
            total, used, free = shutil.disk_usage(target_path)
            free_gb = free / (1024**3)
            used_pct = (used / total) * 100
            self.logger.info(f"Available workspace storage capacity: {free_gb:.2f} GB free ({used_pct:.1f}% used)")
            if used_pct > 90.0:
                self.logger.critical("Workspace disk storage threshold breached risk checkpoint active")
            return free_gb
        except Exception:
            self.logger.warning("Storage volume telemetry metrics checking unavailable")
            return 0.0
