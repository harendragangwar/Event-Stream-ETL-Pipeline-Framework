import unittest
from utils.sanitizer import DataSanitizer
class TestSanitizer(unittest.TestCase):
    def test_clean_string(self):
        dirty_input = "  CLICK!!!123   CORE  "
        res = DataSanitizer.clean_alphanumeric(dirty_input)
        self.assertEqual(res, "CLICK123 CORE")
if __name__ == '__main__':
    unittest.main()
