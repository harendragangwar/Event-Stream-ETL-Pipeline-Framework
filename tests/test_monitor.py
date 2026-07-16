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

    def test_active_io_streams_compliant(self):
        res = self.monitor.verify_active_io_streams(2, max_allowed_streams=4)
        self.assertTrue(res)

    def test_active_io_streams_exceeded(self):
        res = self.monitor.verify_active_io_streams(5, max_allowed_streams=4)
        self.assertFalse(res)
if __name__ == '__main__':
    unittest.main()
