import unittest
import os
import time
from utils.logger import setup_production_logging
from utils.cleanup_engine import PipelineAutoCleanupEngine

class TestCleanupEngine(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.config = {
            "raw_stage_path": "data/test_cleanup_raw",
            "processed_stage_path": "data/test_cleanup_proc",
            "max_staging_directory_retention_hours": 0  # Instant purging test zone
        }
        os.makedirs(self.config["raw_stage_path"], exist_ok=True)
        
        # Creating a dummy transient artifact
        self.test_file = os.path.join(self.config["raw_stage_path"], "stale_run_2026.json")
        with open(self.test_file, "w") as f:
            f.write("{}")

    def tearDown(self):
        for folder in [self.config["raw_stage_path"], self.config["processed_stage_path"]]:
            if os.path.exists(folder):
                import shutil
                try: shutil.rmtree(folder)
                except: pass

    def test_cleanup_engine_retention_purge(self):
        engine = PipelineAutoCleanupEngine(self.logger, self.config)
        deleted = engine.execute_retention_purge()
        self.assertTrue(deleted >= 0)
        self.assertFalse(os.path.exists(self.test_file))
if __name__ == '__main__':
    unittest.main()
