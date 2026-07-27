import os
import sys
from datetime import datetime
from utils.logger import setup_production_logging
from utils.metadata_manager import PipelineMetadataTracker
from utils.exceptions import DataExtractionError, DataTransformationError, DatabaseTransactionError
from utils.system_monitor import PipelineSystemMonitor
from config.settings import get_pipeline_settings
from extractors.log_extractor import RawLogExtractor
from transformers.data_transformer import LogTransformer
from loaders.data_loader import DiskDataLoader
from database.warehouse_engine import DatabaseManager

class DataPipelineCore:
    def __init__(self):
        self.version = "2.0.0"
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.status = "INITIALIZED"
        self.logger = setup_production_logging()
        self._load_config()
        self.extractor = RawLogExtractor(self.logger)
        self.transformer = LogTransformer(self.logger)
        self.loader = DiskDataLoader(self.logger, self.config)
        self.meta_tracker = PipelineMetadataTracker(self.logger)
        self.monitor = PipelineSystemMonitor(self.logger)
        self.db_manager = DatabaseManager(
            self.logger, 
            db_path=self.config["warehouse_db_path"],
            isolation_level=self.config.get("transaction_isolation_level", "DEFERRED")
        )
        self.logger.info(f"Pipeline running version {self.version} network telemetry monitoring core synchronized successfully")

    def _load_config(self):
        self.config = get_pipeline_settings()

    def run_pipeline(self):
        self.logger.info("Executing active partitioned data warehouse framework checkpoints")
        self.status = "RUNNING"
        try:
            current_rss = self.monitor.collect_memory_usage()
            self.monitor.enforce_buffer_limits_check(current_rss, max_limit_mb=self.config.get("memory_buffer_limit_mb", 128.0))
            self.monitor.check_disk_space()
            
            self.monitor.track_key_rotation_status(12, rotation_window_days=self.config.get("encryption_key_rotation_days", 30))
            self.monitor.verify_active_io_streams(1, max_allowed_streams=self.config.get("max_parallel_io_streams", 2))
            
            # Enforce network latency connection pulse validations before loading data models
            self.monitor.verify_heartbeat_telemetry(2, max_interval_sec=self.config.get("network_heartbeat_interval_sec", 5))
            
            target_batch = min(self.config.get("batch_size", 1000), 100)
            raw_data = self.extractor.extract_raw_logs(batch_size=target_batch)
            if len(raw_data) < 1:
                raise DataExtractionError("No data recovered from endpoint")
            self.loader.save_raw_data(raw_data, self.execution_id)
            validated_data = self.transformer.validate_records(raw_data)
            transformed_data = self.transformer.transform_payload(validated_data)
            self.loader.load_processed_data(transformed_data, self.execution_id)
            self.loader.verify_load_sync(self.execution_id)
            self.db_manager.insert_clean_records(transformed_data)
            self.db_manager.compute_activity_metrics()
            self.meta_tracker.generate_run_summary(self.execution_id, len(raw_data), len(transformed_data))
            self.status = "COMPLETED"
        except Exception as e:
            self.status = "FAILED"
            self.logger.error(f"Warehouse partition loop pipeline runtime logic broken: {str(e)}")
            return False
        finally:
            self.monitor.collect_memory_usage()
        return True

if __name__ == "__main__":
    engine = DataPipelineCore()
    engine.run_pipeline()
