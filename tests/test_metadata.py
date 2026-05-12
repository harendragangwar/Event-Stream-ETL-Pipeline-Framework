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

    def test_compliance_matrix_generation_v25(self):
        res = self.tracker.generate_run_summary("run_20260512", 100, 95, meta_dir=self.test_meta_dir)
        self.assertTrue(res["compliance_checks"]["anonymization_applied"])
        self.assertEqual(res["compliance_checks"]["schema_version"], "v2.5")
        self.assertEqual(res["compliance_checks"]["encryption_protocol"], "aes_256_gcm")

    def test_execution_profile_telemetry(self):
        res = self.tracker.generate_run_summary("run_profile_assert", 60, 58, meta_dir=self.test_meta_dir)
        self.assertIn("resource_profiling", res)
        self.assertEqual(res["resource_profiling"]["execution_profile"], "steady_state_batch")
if __name__ == '__main__':
    unittest.main()
