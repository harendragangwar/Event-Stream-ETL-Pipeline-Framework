import logging
from datetime import datetime
from utils.sanitizer import DataSanitizer
class LogTransformer:
    def __init__(self, logger):
        self.logger = logger
    def validate_records(self, data):
        clean_data = []
        for record in data:
            if not record or not record.get("action") or not record.get("event_id"):
                continue
            clean_data.append(record)
        self.logger.info(f"Validation summary matrix verified: {len(clean_data)} passed")
        return clean_data
    def transform_payload(self, data):
        transformed = []
        for record in data:
            payload = record.copy()
            payload["action"] = DataSanitizer.clean_alphanumeric(str(payload["action"]).upper())
            payload["device_type"] = str(payload.get("device_type", "unknown")).lower()
            payload["session_duration_sec"] = int(payload.get("session_duration_sec", 0))
            payload["processed_at"] = datetime.now().isoformat()
            payload["source_system"] = "web_store_front"
            transformed.append(payload)
        return transformed
