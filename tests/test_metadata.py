import unittest
import os
import json
from utils.logger import setup_production_logging
from utils.metadata_manager import PipelineMetadataTracker

class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.tracker = PipelineMetadataTracker(self.logger)
        self.test_meta_dir = "data/test_metadata_runs"

    def tearDown(self):
        if os.path.exists(self.test_meta_dir):
            import shutil
            try: shutil.rmtree(self.test_meta_dir)
            except: pass

    def test_summary_efficiency_calculation(self):
        execution_id = "test_run_20260319"
        res = self.tracker.generate_run_summary(execution_id, 10, 8, meta_dir=self.test_meta_dir)
        
        self.assertEqual(res["metrics"]["total_extracted"], 10)
        self.assertEqual(res["metrics"]["total_processed"], 8)
        self.assertEqual(res["metrics"]["dropped_records"], 2)
        self.assertEqual(res["metrics"]["pipeline_efficiency_pct"], 80.0)
        self.assertEqual(res["environment_telemetry"]["system_status"], "HEALTHY")

    def test_degraded_system_status(self):
        execution_id = "test_run_degraded"
        res = self.tracker.generate_run_summary(execution_id, 10, 5, meta_dir=self.test_meta_dir)
        self.assertEqual(res["environment_telemetry"]["system_status"], "DEGRADED")
