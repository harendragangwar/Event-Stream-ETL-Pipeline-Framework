import unittest
from config.settings import get_pipeline_settings
class TestPipelineConfig(unittest.TestCase):
    def test_config_structure(self):
        settings = get_pipeline_settings()
        self.assertIn("batch_size", settings)
        self.assertIn("warehouse_db_path", settings)
        self.assertEqual(settings["max_retention_days"], 14)
if __name__ == '__main__':
    unittest.main()
