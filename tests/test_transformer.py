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
        self.assertEqual(res[0]["device_type"], "mobile")
        self.assertEqual(res[0]["session_duration_sec"], 500)
if __name__ == '__main__':
    unittest.main()
