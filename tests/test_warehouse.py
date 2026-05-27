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
        self.db_manager = DatabaseManager(self.logger, db_path=self.test_db, isolation_level="DEFERRED")

    def tearDown(self):
        if os.path.exists(self.test_db):
            try: os.remove(self.test_db)
            except: pass

    def test_warehouse_initialization(self):
        self.assertTrue(os.path.exists(self.test_db))

    def test_isolation_level_property(self):
        self.assertEqual(self.db_manager.isolation_level, "DEFERRED")

    def test_attempt_index_column_schema(self):
        mock_record = {
            "event_id": "evt_att_12", "user_id": "usr_12", "action": "CART_ADD",
            "device_type": "mobile", "timestamp": "2026-05-27T00:00:00",
            "processed_at": "2026-05-27T00:01:00", "source_system": "web",
            "session_duration_sec": 120, "partition_key": "thread_2", "attempt_index": 3
        }
        self.db_manager.insert_clean_records([mock_record])
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT attempt_index FROM ecommerce_events WHERE event_id='evt_att_12'")
            val = cursor.fetchone()
        self.assertEqual(val[0], 3)
if __name__ == '__main__':
    unittest.main()
