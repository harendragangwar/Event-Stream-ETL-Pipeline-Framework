import unittest
from utils.sanitizer import DataSanitizer

class TestSanitizer(unittest.TestCase):
    def test_clean_string(self):
        dirty_input = "  CLICK!!!123   CORE  "
        res = DataSanitizer.clean_alphanumeric(dirty_input)
        self.assertEqual(res, "CLICK123 CORE")

    def test_string_truncation_limits(self):
        long_input = "ACTION_" + "X" * 100
        res = DataSanitizer.enforce_string_limits(long_input, max_len=20)
        self.assertEqual(len(res), 20)
        self.assertTrue(res.startswith("ACTION_"))
