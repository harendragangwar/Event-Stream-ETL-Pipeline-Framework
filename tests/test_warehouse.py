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

    def test_invalid_path_exception_handling(self):
        with self.assertRaises(DatabaseTransactionError):
            broken_manager = DatabaseManager(self.logger, db_path="/invalid_dir/null.db")
            broken_manager.insert_clean_records([{"event_id": "evt_100"}])
if __name__ == '__main__':
    unittest.main()
