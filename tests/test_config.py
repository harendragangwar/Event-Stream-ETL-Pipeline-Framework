import unittest
from config.settings import get_pipeline_settings
class TestPipelineConfig(unittest.TestCase):
    def test_config_structure(self):
        settings = get_pipeline_settings()
        self.assertIn("batch_size", settings)
        self.assertEqual(settings["batch_size"], 1500)
        self.assertFalse(settings["is_production"])
if __name__ == '__main__':
    unittest.main()
