import os
import sys
from datetime import datetime
from utils.logger import setup_production_logging
from utils.metadata_manager import PipelineMetadataTracker
from utils.exceptions import DataExtractionError, DataTransformationError
from config.settings import get_pipeline_settings
from extractors.log_extractor import RawLogExtractor
from transformers.data_transformer import LogTransformer
from loaders.data_loader import DiskDataLoader
class DataPipelineCore:
    def __init__(self):
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.status = "INITIALIZED"
        self.logger = setup_production_logging()
        self._load_config()
        self.extractor = RawLogExtractor(self.logger)
        self.transformer = LogTransformer(self.logger)
        self.loader = DiskDataLoader(self.logger, self.config)
        self.meta_tracker = PipelineMetadataTracker(self.logger)
        self.logger.info(f"Pipeline Run ID {self.execution_id} launched successfully")
    def _load_config(self):
        self.config = get_pipeline_settings()
        self.logger.info(f"Pipeline settings system loaded for environment: {self.config['environment']}")
    def run_pipeline(self):
        self.logger.info("Executing active data node checkpoints")
        self.status = "RUNNING"
        try:
            raw_data = self.extractor.extract_raw_logs()
            if not raw_data:
                raise DataExtractionError("No data recovered from endpoint")
            self.loader.save_raw_data(raw_data, self.execution_id)
            validated_data = self.transformer.validate_records(raw_data)
            transformed_data = self.transformer.transform_payload(validated_data)
            self.loader.load_processed_data(transformed_data, self.execution_id)
            self.meta_tracker.generate_run_summary(self.execution_id, len(raw_data), len(transformed_data))
        except Exception as e:
            self.status = "FAILED"
            self.logger.error(f"Pipeline crashed during execution lifecycle: {str(e)}")
            return False
        return True
if __name__ == "__main__":
    engine = DataPipelineCore()
    engine.run_pipeline()
