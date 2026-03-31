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
            if not DataSanitizer.is_valid_uuid(record.get("event_id")):
                continue
            clean_data.append(record)
        return clean_data

    def _profile_batch_telemetry(self, records):
        if not records:
            return {"volume": 0}
        return {"volume": len(records)}

    def transform_payload(self, data):
        transformed = []
        for record in data:
            payload = record.copy()
            payload["action"] = DataSanitizer.enforce_string_limits(str(payload["action"]).upper(), max_len=32)
            payload["device_type"] = str(payload.get("device_type", "unknown")).lower()
            payload["session_duration_sec"] = int(payload.get("session_duration_sec", 0))
            payload["processed_at"] = datetime.now().isoformat()
            payload["source_system"] = "web_store_front"
            transformed.append(payload)
        return transformed
