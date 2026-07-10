import unittest
import os
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

    def test_compliance_matrix_generation_v26(self):
        res = self.tracker.generate_run_summary("run_20260710", 100, 95, meta_dir=self.test_meta_dir)
        self.assertTrue(res["compliance_checks"]["anonymization_applied"])
        self.assertEqual(res["compliance_checks"]["schema_version"], "v2.6")
        self.assertEqual(res["environment_telemetry"]["engine_version"], "1.8.6")

    def test_key_rotation_check_telemetry_indicator(self):
        res = self.tracker.generate_run_summary("run_rotation_meta_assert", 70, 68, meta_dir=self.test_meta_dir)
        self.assertIn("resource_profiling", res)
        self.assertTrue(res["resource_profiling"]["key_rotation_check_applied"])
        self.assertTrue(res["resource_profiling"]["anomaly_profiling_enabled"])
if __name__ == '__main__':
    unittest.main()
