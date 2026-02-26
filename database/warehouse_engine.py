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
        with sqlite3.connect(self.db_path) as conn:
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
        self.logger.info("Local storage warehouse structures initialized successfully")
    def insert_clean_records(self, record_list):
        if not record_list:
            return
        inserted_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for rec in record_list:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO ecommerce_events 
                        (event_id, user_id, action, device_type, timestamp, processed_at, source_system)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        rec.get("event_id"), rec.get("user_id"), rec.get("action"),
                        rec.get("device_type"), rec.get("timestamp"), rec.get("processed_at"),
                        rec.get("source_system")
                    ))
                    inserted_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to insert row token {rec.get('event_id')}: {str(e)}")
            conn.commit()
        self.logger.info(f"Database sink transaction completed. Synced {inserted_count} table records")
