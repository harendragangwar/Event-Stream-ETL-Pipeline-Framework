import random
from datetime import datetime
class RawLogExtractor:
    def __init__(self, logger):
        self.logger = logger
    def extract_raw_logs(self):
        self.logger.info("Starting mock data extraction from source endpoint")
        events = ["click", "view", "purchase", "cart_add"]
        mock_data = []
        for i in range(10):
            record = {
                "event_id": f"evt_{random.randint(1000, 9999)}",
                "timestamp": datetime.now().isoformat(),
                "action": random.choice(events) if random.random() > 0.1 else None,
                "user_id": f"usr_{random.randint(1, 100)}",
                "device_type": random.choice(["mobile", "desktop", "tablet"])
            }
            mock_data.append(record)
        self.logger.info(f"Successfully extracted {len(mock_data)} raw event logs")
        return mock_data
