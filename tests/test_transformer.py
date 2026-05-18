import unittest
from transformers.data_transformer import LogTransformer
from utils.logger import setup_production_logging

class TestTransformer(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.transformer = LogTransformer(self.logger)

    def test_payload_transformation_bounds(self):
        mock_raw = [{"event_id": "evt_123", "action": "click", "device_type": "MOBILE", "session_duration_sec": "500"}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(res[0]["action"], "CLICK")
        self.assertEqual(res[0]["device_type"], "mobile")

    def test_attempt_index_mapping(self):
        mock_raw = [{"event_id": "evt_555", "action": "view", "extraction_attempt": 2}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(res[0]["attempt_index"], 2)

    def test_injection_safe_payload_transform(self):
        mock_raw = [{"event_id": "evt_456", "action": "purchase; DROP TABLE users; --", "device_type": "desktop"}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertNotIn(";", res[0]["action"])
        self.assertTrue(res[0]["action"].startswith("PURCHASE DROP"))
if __name__ == '__main__':
    unittest.main()
