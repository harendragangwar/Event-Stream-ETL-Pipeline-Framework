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

    def test_extended_metrics_aggregation_fields(self):
        mock_records = [
            {"event_id": "evt_v1", "user_id": "usr_x", "action": "VIEW", "device_type": "mobile", "timestamp": "2026", "processed_at": "2026", "source_system": "web", "session_duration_sec": 300},
            {"event_id": "evt_v2", "user_id": "usr_y", "action": "VIEW", "device_type": "mobile", "timestamp": "2026", "processed_at": "2026", "source_system": "web", "session_duration_sec": 600}
        ]
        self.db_manager.insert_clean_records(mock_records)
        compiled = self.db_manager.compute_activity_metrics()
        
        self.assertIn("actions", compiled)
        self.assertEqual(compiled["actions"]["VIEW"]["count"], 2)
        self.assertEqual(compiled["actions"]["VIEW"]["avg_duration"], 450.0)
        self.assertEqual(compiled["actions"]["VIEW"]["total_volume_sec"], 900)
        self.assertIn("generated_at", compiled)
if __name__ == '__main__':
    unittest.main()
