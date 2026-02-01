import os
import psutil
class PipelineSystemMonitor:
    def __init__(self, logger):
        self.logger = logger
    def collect_memory_usage(self):
        try:
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
            self.logger.info(f"Pipeline memory consumption: {mem_mb:.2f} MB")
            return mem_mb
        except Exception:
            self.logger.warning("Native process telemetry profiling unavailable")
            return 0.0
