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
        self.assertEqual(res["action"], "CLICK")
        self.assertEqual(res["device_type"], "mobile")

    def test_injection_safe_payload_transform(self):
        mock_raw = [{"event_id": "evt_456", "action": "purchase; DROP TABLE users; --", "device_type": "desktop"}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertNotIn(";", res["action"])
        self.assertNotIn("-", res["action"])
        self.assertTrue(res["action"].startswith("PURCHASE DROP"))

    def test_stream_partition_key_assignment(self):
        mock_raw = [{"event_id": "evt_777", "action": "purchase", "device_type": "tablet", "extraction_thread_id": 3}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(res["partition_key"], "thread_3")
if __name__ == '__main__':
    unittest.main()
