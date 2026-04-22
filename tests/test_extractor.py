import unittest
from extractors.log_extractor import RawLogExtractor
from utils.logger import setup_production_logging

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.extractor = RawLogExtractor(self.logger)

    def test_extraction_count_default(self):
        data = self.extractor.extract_raw_logs(batch_size=10)
        self.assertEqual(len(data), 10)

    def test_thread_allocation_metadata(self):
        data = self.extractor.extract_raw_logs(batch_size=5)
        for record in data:
            self.assertIn("extraction_thread_id", record)
            self.assertTrue(1 <= record["extraction_thread_id"] <= 4)
if __name__ == '__main__':
    unittest.main()
