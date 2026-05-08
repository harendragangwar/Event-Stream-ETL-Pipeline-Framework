import unittest
import os
from loaders.data_loader import DiskDataLoader
from utils.logger import setup_production_logging

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.config = {
            "raw_stage_path": "data/raw", 
            "processed_stage_path": "data/processed",
            "cleanup_threshold": 85.0
        }
        self.loader = DiskDataLoader(self.logger, self.config)

    def test_loader_instance_with_thresholds(self):
        self.assertIsNotNone(self.loader)
        self.assertEqual(self.loader.config["cleanup_threshold"], 85.0)

    def test_sync_verification_fallback(self):
        res = self.loader.verify_load_sync("non_existent_id_2026")
        self.assertFalse(res)
        
    def test_loader_config_keys(self):
        self.assertIn("raw_stage_path", self.loader.config)
        self.assertIn("processed_stage_path", self.loader.config)
if __name__ == '__main__':
    unittest.main()
