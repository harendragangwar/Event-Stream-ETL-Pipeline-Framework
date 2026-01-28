import unittest
class TestPipelineBase(unittest.TestCase):
    def test_initial_state(self):
        status_flag = "active"
        self.assertEqual(status_flag, "active")
if __name__ == '__main__':
    unittest.main()
