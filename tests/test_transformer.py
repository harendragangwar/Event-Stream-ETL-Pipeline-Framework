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

    def test_stream_partition_key_assignment(self):
        mock_raw = [{"event_id": "evt_777", "action": "purchase", "device_type": "tablet", "extraction_thread_id": 3}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(res[0]["partition_key"], "thread_3")

    def test_string_limit_truncation(self):
        long_action = "BURST_ACTION_" + "X" * 100
        mock_raw = [{"event_id": "evt_999", "action": long_action, "device_type": "desktop"}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertEqual(len(res[0]["action"]), 64)
        self.assertTrue(res[0]["action"].startswith("BURST_ACTION_"))
if __name__ == '__main__':
    unittest.main()
