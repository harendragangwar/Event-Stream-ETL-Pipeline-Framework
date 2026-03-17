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

    def test_batch_telemetry_profiling(self):
        mock_batch = [
            {"event_id": "1", "device_type": "desktop"},
            {"event_id": "2", "device_type": "mobile"},
            {"event_id": "3", "device_type": "desktop"}
        ]
        metrics = self.transformer._profile_batch_telemetry(mock_batch)
        self.assertEqual(metrics["dominant_device"], "desktop")
        self.assertEqual(metrics["volume"], 3)
        self.assertIn("calculated_at", metrics)

    def test_empty_batch_telemetry(self):
        metrics = self.transformer._profile_batch_telemetry([])
        self.assertEqual(metrics["dominant_device"], "none")
        self.assertEqual(metrics["volume"], 0)
