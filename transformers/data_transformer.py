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

    def _profile_batch_telemetry(self, records):
        if not records:
            return {"dominant_device": "none", "volume": 0}
        devices = [r.get("device_type", "unknown") for r in records]
        most_frequent = max(set(devices), key=devices.count)
        profile_summary = {
            "dominant_device": most_frequent,
            "volume": len(records),
            "calculated_at": datetime.now().isoformat()
        }
        self.logger.info(f"Batch transformation telemetry profiling metrics computed: {str(profile_summary)}")
        return profile_summary

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
        self._profile_batch_telemetry(transformed)
        return transformed
