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

    def test_enforce_buffer_limits_valid(self):
        res = self.monitor.enforce_buffer_limits_check(50.0, max_limit_mb=128.0)
        self.assertTrue(res)

    def test_enforce_buffer_limits_breached(self):
        res = self.monitor.enforce_buffer_limits_check(200.0, max_limit_mb=128.0)
        self.assertFalse(res)
if __name__ == '__main__':
    unittest.main()
