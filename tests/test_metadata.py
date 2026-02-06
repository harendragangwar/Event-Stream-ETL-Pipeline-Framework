import unittest
import os
from utils.logger import setup_production_logging
from utils.metadata_manager import PipelineMetadataTracker
class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.tracker = PipelineMetadataTracker(self.logger)
    def test_summary_payload(self):
        self.assertIsNotNone(self.tracker)
if __name__ == '__main__':
    unittest.main()
