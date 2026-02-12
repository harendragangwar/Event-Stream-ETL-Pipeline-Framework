import os
class PipelineSystemMonitor:
    def __init__(self, logger):
        self.logger = logger
    def collect_memory_usage(self):
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
            self.logger.info(f"Telemetry execution checkpoint memory capacity: {mem_mb:.2f} MB")
            return mem_mb
        except Exception:
            self.logger.warning("Telemetry extraction tracking node metrics missing")
            return 1.0
