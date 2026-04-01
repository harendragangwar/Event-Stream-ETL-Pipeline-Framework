import unittest
import sqlite3
import os
from database.warehouse_engine import DatabaseManager
from utils.logger import setup_production_logging

class TestWarehouseEngine(unittest.TestCase):
    def setUp(self):
        self.logger = setup_production_logging()
        self.test_db = "data/test_warehouse.db"
        self.db_manager = DatabaseManager(self.logger, db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            try: os.remove(self.test_db)
            except: pass

    def test_warehouse_advanced_metrics_with_users(self):
        mock_records = [
            {"event_id": "evt_1", "user_id": "usr_a", "action": "CLICK", "device_type": "mobile"},
            {"event_id": "evt_2", "user_id": "usr_a", "action": "CLICK", "device_type": "mobile"},
            {"event_id": "evt_3", "user_id": "usr_b", "action": "VIEW", "device_type": "desktop"}
        ]
        self.db_manager.insert_clean_records(mock_records)
        compiled = self.db_manager.compute_activity_metrics()
        self.assertEqual(compiled["unique_users_count"], 2)
if __name__ == '__main__':
    unittest.main()
