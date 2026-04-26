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
            "device_type": "desktop", "timestamp": "2026-04-26T00:00:00",
            "processed_at": "2026-04-26T00:01:00", "source_system": "web",
            "session_duration_sec": 420, "partition_key": "thread_4"
        }
        self.db_manager.insert_clean_records([mock_record])
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT partition_key FROM ecommerce_events WHERE event_id='evt_part_99'")
            val = cursor.fetchone()
        self.assertEqual(val[0], "thread_4")
if __name__ == '__main__':
    unittest.main()
