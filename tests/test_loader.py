import unittest
import os
from loaders.data_loader import DiskDataLoader
from utils.logger import setup_production_logging

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.config = {"raw_stage_path": "data/raw", "processed_stage_path": "data/processed"}
        self.loader = DiskDataLoader(self.logger, self.config)

    def test_verify_load_sync_nonexistent(self):
        res = self.loader.verify_load_sync("null_token_id")
        self.assertFalse(res)
if __name__ == '__main__':
    unittest.main()
