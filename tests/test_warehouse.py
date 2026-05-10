import unittest
import sqlite3
import os
from database.warehouse_engine import DatabaseManager
from utils.logger import setup_production_logging
from utils.exceptions import DatabaseTransactionError

class TestWarehouseEngine(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.test_db = "data/test_warehouse.db"
        self.db_manager = DatabaseManager(self.logger, db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            try: os.remove(self.test_db)
            except: pass

    def test_warehouse_initialization(self):
        self.assertTrue(os.path.exists(self.test_db))

    def test_partition_key_records_insertion(self):
        mock_record = {
            "event_id": "evt_part_99", "user_id": "usr_99", "action": "PURCHASE",
            "device_type": "desktop", "timestamp": "2026-05-10T00:00:00",
            "processed_at": "2026-05-10T00:01:00", "source_system": "web",
            "session_duration_sec": 420, "partition_key": "thread_4"
        }
        self.db_manager.insert_clean_records([mock_record])
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT partition_key FROM ecommerce_events WHERE event_id='evt_part_99'")
            val = cursor.fetchone()
        self.assertEqual(val[0], "thread_4")

    def test_integrity_check_verification_marker(self):
        mock_record = {
            "event_id": "evt_marker_1", "user_id": "usr_1", "action": "CLICK",
            "device_type": "mobile", "timestamp": "2026", "processed_at": "2026"
        }
        self.db_manager.insert_clean_records([mock_record])
        compiled = self.db_manager.compute_activity_metrics()
        self.assertIn("verification_status", compiled)
        self.assertEqual(compiled["verification_status"], "INTEGRITY_CHECK_PASS")
if __name__ == '__main__':
    unittest.main()
