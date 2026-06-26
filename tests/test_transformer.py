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

    def test_anomaly_flag_evaluation_triggered(self):
        mock_raw = [{"event_id": "evt_anomaly_high", "action": "view", "session_duration_sec": 1750}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertTrue(res[0]["is_anomaly_detected"])

    def test_anomaly_flag_evaluation_normal(self):
        mock_raw = [{"event_id": "evt_anomaly_low", "action": "view", "session_duration_sec": 450}]
        res = self.transformer.transform_payload(mock_raw)
        self.assertFalse(res[0]["is_anomaly_detected"])
if __name__ == '__main__':
    unittest.main()
