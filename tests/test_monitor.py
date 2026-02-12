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
if __name__ == '__main__':
    unittest.main()
