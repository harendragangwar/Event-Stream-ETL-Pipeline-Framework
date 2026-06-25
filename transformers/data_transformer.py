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
            safe_action = DataSanitizer.strip_sql_injection_chars(str(payload["action"]))
            payload["action"] = DataSanitizer.enforce_string_limits(safe_action.upper(), max_len=64)
            payload["device_type"] = str(payload.get("device_type", "unknown")).lower()
            payload["session_duration_sec"] = int(payload.get("session_duration_sec", 0))
            payload["processed_at"] = datetime.now().isoformat()
            payload["source_system"] = "web_store_front"
            payload["partition_key"] = f"thread_{payload.get('extraction_thread_id', 1)}"
            payload["attempt_index"] = int(payload.get("extraction_attempt", 1))
            
            # Dynamic Anomaly evaluation logic
            duration = payload["session_duration_sec"]
            payload["is_anomaly_detected"] = True if duration > 1500 or duration < 5 else False
            
            transformed.append(payload)
        return transformed
