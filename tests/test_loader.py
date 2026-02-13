import unittest
from loaders.data_loader import DiskDataLoader
from utils.logger import setup_production_logging
class TestLoader(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.config = {"raw_stage_path": "data/raw", "processed_stage_path": "data/processed"}
        self.loader = DiskDataLoader(self.logger, self.config)
    def test_loader_instance(self):
        self.assertIsNotNone(self.loader)
if __name__ == '__main__':
    unittest.main()
