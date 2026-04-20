import unittest
import os
from config.settings import get_pipeline_settings

class TestPipelineConfig(unittest.TestCase):
    def test_config_structure_default_dev(self):
        if "PIPELINE_ENV" in os.environ:
            del os.environ["PIPELINE_ENV"]
        settings = get_pipeline_settings()
        self.assertEqual(settings["batch_size"], 1000)
        self.assertEqual(settings["max_threads"], 1)
        self.assertFalse(settings["is_production"])

    def test_config_structure_production_profile(self):
        os.environ["PIPELINE_ENV"] = "prod"
        settings = get_pipeline_settings()
        self.assertEqual(settings["batch_size"], 5000)
        self.assertEqual(settings["max_threads"], 4)
        self.assertTrue(settings["is_production"])
        del os.environ["PIPELINE_ENV"]
if __name__ == '__main__':
    unittest.main()
