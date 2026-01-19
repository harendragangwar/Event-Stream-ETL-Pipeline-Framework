import logging
from datetime import datetime

class LogTransformer:
    def __init__(self, logger):
        self.logger = logger

    def validate_records(self, data):
        clean_data = []
        for record in data:
            if not record.get("action") or not record.get("event_id"):
                self.logger.warning(f"Skipping bad record missing critical fields: {record['event_id']}")
                continue
            clean_data.append(record)
        self.logger.info(f"Validation complete. Passed: {len(clean_data)}/{len(data)}")
        return clean_data

    def transform_payload(self, data):
        transformed = []
        for record in data:
            payload = record.copy()
            payload["action"] = str(payload["action"]).upper()
            payload["processed_at"] = datetime.now().isoformat()
            payload["source_system"] = "web_store_front"
            transformed.append(payload)
        self.logger.info(f"Transformation node applied formatting to {len(transformed)} nodes")
        return transformed
