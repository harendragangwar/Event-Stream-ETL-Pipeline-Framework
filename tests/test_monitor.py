import unittest
from utils.logger import setup_production_logging
from utils.system_monitor import PipelineSystemMonitor

class TestSystemMonitor(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.monitor = PipelineSystemMonitor(self.logger)

    def test_telemetry_execution(self):
        res = self.monitor.collect_memory_usage()
        self.assertTrue(res >= 0.0)

    def test_storage_telemetry_bounds(self):
        free_gb = self.monitor.check_disk_space()
        self.assertIsInstance(free_gb, float)
        self.assertTrue(free_gb >= 0.0)

    def test_key_rotation_status_compliant(self):
        res = self.monitor.track_key_rotation_status(15, rotation_window_days=30)
        self.assertTrue(res)

    def test_key_rotation_status_breached(self):
        res = self.monitor.track_key_rotation_status(35, rotation_window_days=30)
        self.assertFalse(res)
if __name__ == '__main__':
    unittest.main()
