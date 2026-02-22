import sqlite3
import os
class DatabaseManager:
    def __init__(self, logger, db_path="data/pipeline_warehouse.db"):
        self.logger = logger
        self.db_path = db_path
        self._initialize_warehouse()
    def _initialize_warehouse(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ecommerce_events (
                event_id TEXT PRIMARY KEY,
                user_id TEXT,
                action TEXT,
                device_type TEXT,
                timestamp TEXT,
                processed_at TEXT,
                source_system TEXT
            )
        ''')
        conn.commit()
        conn.close()
        self.logger.info("Local storage warehouse structures initialized successfully")
