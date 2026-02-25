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
    def test_warehouse_initialization(self):
        self.assertTrue(os.path.exists(self.test_db))
    def test_record_insertion_empty(self):
        self.db_manager.insert_clean_records([])
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ecommerce_events")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)
if __name__ == '__main__':
    unittest.main()
