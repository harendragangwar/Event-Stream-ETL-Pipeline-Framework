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
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
        self.assertEqual(mode.lower(), "wal")

    def test_invalid_path_exception(self):
        with self.assertRaises(DatabaseTransactionError):
            broken_manager = DatabaseManager(self.logger, db_path="/invalid_dir/null.db")

    def test_session_records_insertion(self):
        mock_record = {
            "event_id": "evt_test_1", "user_id": "usr_1", "action": "CLICK",
            "device_type": "mobile", "timestamp": "2026-03-21T00:00:00",
            "processed_at": "2026-03-21T00:01:00", "source_system": "web",
            "session_duration_sec": 350
        }
        self.db_manager.insert_clean_records([mock_record])
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_duration_sec FROM ecommerce_events WHERE event_id='evt_test_1'")
            val = cursor.fetchone()[0]
        self.assertEqual(val, 350)
if __name__ == '__main__':
    unittest.main()
