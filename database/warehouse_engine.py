import sqlite3
import os
from utils.exceptions import DatabaseTransactionError

class DatabaseManager:
    def __init__(self, logger, db_path="data/pipeline_warehouse.db"):
        self.logger = logger
        self.db_path = db_path
        self._initialize_warehouse()

    def _initialize_warehouse(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        try:
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA synchronous=NORMAL;")
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ecommerce_events (
                        event_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        action TEXT,
                        device_type TEXT,
                        timestamp TEXT,
                        processed_at TEXT,
                        source_system TEXT,
                        session_duration_sec INTEGER
                    )
                ''')
                conn.commit()
        except Exception as e:
            raise DatabaseTransactionError(f"Warehouse setup crash: {str(e)}")
        self.logger.info("Storage warehouse optimization completed with WAL pooling configurations")

    def insert_clean_records(self, record_list):
        if not record_list:
            return
        inserted_count = 0
        try:
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                for rec in record_list:
                    cursor.execute('''
                        INSERT OR REPLACE INTO ecommerce_events 
                        (event_id, user_id, action, device_type, timestamp, processed_at, source_system, session_duration_sec)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        rec.get("event_id"), rec.get("user_id"), rec.get("action"),
                        rec.get("device_type"), rec.get("timestamp"), rec.get("processed_at"),
                        rec.get("source_system"), rec.get("session_duration_sec", 0)
                    ))
                    inserted_count += 1
                conn.commit()
        except Exception as e:
            raise DatabaseTransactionError(f"Database write failure: {str(e)}")
        self.logger.info(f"Database sink transaction completed. Synced {inserted_count} table records")

    def compute_activity_metrics(self):
        try:
            with sqlite3.connect(self.db_path, timeout=30.0) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT action, COUNT(*), AVG(session_duration_sec) FROM ecommerce_events GROUP BY action')
                metrics = cursor.fetchall()
                action_summary = {action: {"count": count, "avg_duration": round(avg_dur, 2)} for action, count, avg_dur in metrics}
                
                cursor.execute('SELECT device_type, COUNT(*) FROM ecommerce_events GROUP BY device_type')
                device_metrics = cursor.fetchall()
                device_summary = {device: count for device, count in device_metrics}
                
                cursor.execute('SELECT COUNT(DISTINCT user_id) FROM ecommerce_events')
                unique_users = cursor.fetchone()[0]
                
                compiled_metrics = {
                    "actions": action_summary,
                    "devices": device_summary,
                    "unique_users_count": unique_users
                }
                self.logger.info(f"Warehouse advanced metrics compiled with user metrics: {str(compiled_metrics)}")
                return compiled_metrics
        except Exception as e:
            self.logger.error(f"Failed to query database metric states: {str(e)}")
            return {}
