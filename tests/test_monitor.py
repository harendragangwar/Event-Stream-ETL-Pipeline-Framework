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

    def test_heartbeat_telemetry_compliant(self):
        res = self.monitor.verify_heartbeat_telemetry(3, max_interval_sec=5)
        self.assertTrue(res)

    def test_heartbeat_telemetry_breached(self):
        res = self.monitor.verify_heartbeat_telemetry(8, max_interval_sec=5)
        self.assertFalse(res)
if __name__ == '__main__':
    unittest.main()
