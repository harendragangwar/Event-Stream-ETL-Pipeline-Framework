import unittest
from transformers.data_transformer import LogTransformer
from utils.logger import setup_production_logging

class TestTransformer(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.transformer = LogTransformer(self.logger)

    def test_payload_transformation(self):
        mock_raw = [{"event_id": "evt_123", "action": "click", "device_type": "MOBILE", "session_duration_sec": "500"}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(res[0]["action"], "CLICK")

    def test_invalid_uuid_discard(self):
        mock_raw = [{"event_id": "corrupted_id", "action": "click"}]
        res = self.transformer.validate_records(mock_raw)
        self.assertEqual(len(res), 0)
if __name__ == '__main__':
    unittest.main()
