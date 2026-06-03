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

    def test_transaction_sync_signatures(self):
        mock_record = {
            "event_id": "evt_sync_101", "user_id": "usr_101", "action": "CLICK",
            "device_type": "desktop", "timestamp": "2026-06-03T00:00:00",
            "processed_at": "2026-06-03T00:01:00", "source_system": "web",
            "session_duration_sec": 45, "partition_key": "thread_1", "attempt_index": 1
        }
        self.db_manager.insert_clean_records([mock_record])
        compiled = self.db_manager.compute_activity_metrics()
        self.assertEqual(compiled["verification_status"], "INTEGRITY_CHECK_PASS")
if __name__ == '__main__':
    unittest.main()
