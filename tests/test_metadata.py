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
        res = self.tracker.generate_run_summary("run_20260827", 100, 95, meta_dir=self.test_meta_dir)
        self.assertTrue(res["compliance_checks"]["anonymization_applied"])
        self.assertEqual(res["compliance_checks"]["schema_version"], "v2.6")

    def test_staging_directory_retention_verified_telemetry_indicator(self):
        res = self.tracker.generate_run_summary("run_staging_meta_assert", 90, 89, meta_dir=self.test_meta_dir)
        self.assertIn("resource_profiling", res)
        self.assertTrue(res["resource_profiling"]["staging_directory_retention_verified"])
        self.assertTrue(res["resource_profiling"]["storage_sector_cache_verified"])
if __name__ == '__main__':
    unittest.main()
