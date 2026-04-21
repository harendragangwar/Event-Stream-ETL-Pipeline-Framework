import random
import time
from datetime import datetime

class RawLogExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_raw_logs(self, batch_size=50):
        self.logger.info("Starting multi-threaded simulated data extraction from source endpoint")
        start_time = time.time()
        events = ["click", "view", "purchase", "cart_add"]
        mock_data = []
        for i in range(batch_size):
            record = {
                "event_id": f"evt_{random.randint(10000, 99999)}",
                "timestamp": datetime.now().isoformat(),
                "action": random.choice(events) if random.random() > 0.05 else None,
                "user_id": f"usr_{random.randint(100, 999)}",
                "device_type": random.choice(["mobile", "desktop", "tablet"]),
                "session_duration_sec": random.randint(10, 1800),
                "extraction_thread_id": random.randint(1, 4)
            }
            mock_data.append(record)
        self.logger.info(f"Successfully extracted {len(mock_data)} raw event logs across active partitions in {time.time() - start_time:.4f}s")
        return mock_data
