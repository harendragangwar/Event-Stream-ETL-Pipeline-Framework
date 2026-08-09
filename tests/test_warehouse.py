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

    def test_storage_sector_optimization_flag_assert(self):
        mock_record = {
            "event_id": "evt_sector_opt_4", "user_id": "usr_sector_4", "action": "CLICK",
            "device_type": "desktop", "timestamp": "2026-08-09T00:00:00",
            "processed_at": "2026-08-09T00:01:00", "source_system": "web"
        }
        self.db_manager.insert_clean_records([mock_record])
        compiled = self.db_manager.compute_activity_metrics()
        self.assertIn("storage_sector_optimized", compiled)
        self.assertTrue(compiled["storage_sector_optimized"])
        self.assertEqual(compiled["verification_status"], "INTEGRITY_CHECK_PASS")
if __name__ == '__main__':
    unittest.main()
