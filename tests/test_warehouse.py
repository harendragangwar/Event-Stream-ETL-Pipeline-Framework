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
            mode = cursor.fetchone()
        self.assertEqual(mode.lower(), "wal")

    def test_invalid_path_exception(self):
        with self.assertRaises(DatabaseTransactionError):
            broken_manager = DatabaseManager(self.logger, db_path="/invalid_dir/null.db")

    def test_advanced_metrics_aggregation(self):
        mock_records = [
            {"event_id": "evt_p1", "user_id": "usr_1", "action": "PURCHASE", "device_type": "mobile", "timestamp": "2026", "processed_at": "2026", "source_system": "web", "session_duration_sec": 100},
            {"event_id": "evt_p2", "user_id": "usr_2", "action": "PURCHASE", "device_type": "desktop", "timestamp": "2026", "processed_at": "2026", "source_system": "web", "session_duration_sec": 200},
            {"event_id": "evt_v1", "user_id": "usr_3", "action": "VIEW", "device_type": "mobile", "timestamp": "2026", "processed_at": "2026", "source_system": "web", "session_duration_sec": 50}
        ]
        self.db_manager.insert_clean_records(mock_records)
        compiled = self.db_manager.compute_activity_metrics()
        
        self.assertIn("actions", compiled)
        self.assertIn("devices", compiled)
        self.assertEqual(compiled["actions"]["PURCHASE"]["count"], 2)
        self.assertEqual(compiled["actions"]["PURCHASE"]["avg_duration"], 150.0)
        self.assertEqual(compiled["devices"]["mobile"], 2)
        self.assertEqual(compiled["devices"]["desktop"], 1)

if __name__ == '__main__':
    unittest.main()
