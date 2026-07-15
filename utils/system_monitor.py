import os
import sys

class PipelineSystemMonitor:
    def __init__(self, logger):
        self.logger = logger

    def collect_memory_usage(self):
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            mem_mb = mem_info.rss / (1024 * 1024)
            virt_mem_mb = mem_info.vms / (1024 * 1024)
            shared_mem_mb = getattr(mem_info, 'shared', 0) / (1024 * 1024)
            cpu_usage_pct = process.cpu_percent(interval=None)
            
            self.logger.info(
                f"System physical footprint: {mem_mb:.2f} MB | "
                f"Virtual allocation: {virt_mem_mb:.2f} MB | "
                f"Shared segment: {shared_mem_mb:.2f} MB | "
                f"Core CPU usage: {cpu_usage_pct:.1f}%"
            )
            return mem_mb
        except Exception:
            self.logger.warning("Native process telemetry profiling metrics missing or offline")
            return 0.0

    def enforce_buffer_limits_check(self, current_allocated_mb, max_limit_mb=128.0):
        if current_allocated_mb > max_limit_mb:
            self.logger.warning(f"Telemetry heap tracking limits exceeded: {current_allocated_mb:.2f}MB breached threshold bounds: {max_limit_mb:.2f}MB")
            return False
        self.logger.info(f"System memory tracking diagnostics verified safely inside threshold buffer boundaries")
        return True

    def track_key_rotation_status(self, current_age_days, rotation_window_days=30):
        if current_age_days >= rotation_window_days:
            self.logger.warning(f"Cryptographic threshold marker reached: Token age {current_age_days} days breaches rotation policy: {rotation_window_days} days")
            return False
        self.logger.info(f"Platform cryptographic rotation bounds clear. Next cycle scheduled within compliance matrix rules")
        return True

    def verify_active_io_streams(self, active_count, max_allowed_streams=2):
        if active_count > max_allowed_streams:
            self.logger.critical(f"I/O stream threshold exceeded: Active {active_count} concurrent streams breach configuration limit: {max_allowed_streams}")
            return False
        self.logger.info(f"Concurrent workflow streams verified inside pipeline safety boundaries: {active_count}/{max_allowed_streams}")
        return True

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
