import unittest
import os
from config.settings import get_pipeline_settings

class TestPipelineConfig(unittest.TestCase):
    def test_config_structure_default_dev(self):
        if "PIPELINE_ENV" in os.environ:
            del os.environ["PIPELINE_ENV"]
        settings = get_pipeline_settings()
        self.assertEqual(settings["batch_size"], 1000)
        self.assertEqual(settings["max_retention_days"], 7)
        self.assertFalse(settings["enable_compression"])
        self.assertEqual(settings["cleanup_threshold"], 95.0)

    def test_config_structure_production_profile(self):
        os.environ["PIPELINE_ENV"] = "prod"
        settings = get_pipeline_settings()
        self.assertEqual(settings["batch_size"], 5000)
        self.assertEqual(settings["max_retention_days"], 30)
        self.assertTrue(settings["enable_compression"])
        self.assertEqual(settings["cleanup_threshold"], 85.0)
        del os.environ["PIPELINE_ENV"]
if __name__ == '__main__':
    unittest.main()
