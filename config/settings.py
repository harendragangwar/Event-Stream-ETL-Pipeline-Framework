import os

def get_pipeline_settings():
    env_mode = os.getenv("PIPELINE_ENV", "dev")
    config_profiles = {
        "prod": {
            "batch_size": 5000,
            "retry_limit": 5,
            "timeout": 120,
            "max_retention_days": 30,
            "enable_compression": True,
            "cleanup_threshold_pct": 85.0,
            "max_network_threads": 4,
            "backup_retention_limit": 5,
            "isolation_level": "EXCLUSIVE",
            "buffer_limit_mb": 512.0,
            "compression_size_kb": 1024,
            "anomaly_threshold": 0.01,
            "rotation_days": 90,
            "io_streams": 8,
            "heartbeat_sec": 15
        },
        "dev": {
            "batch_size": 1000,
            "retry_limit": 3,
            "timeout": 45,
            "max_retention_days": 7,
            "enable_compression": False,
            "cleanup_threshold_pct": 95.0,
            "max_network_threads": 1,
            "backup_retention_limit": 2,
            "isolation_level": "DEFERRED",
            "buffer_limit_mb": 128.0,
            "compression_size_kb": 256,
            "anomaly_threshold": 0.05,
            "rotation_days": 30,
            "io_streams": 2,
            "heartbeat_sec": 5
        }
    }
    
    selected_profile = config_profiles.get(env_mode.lower(), config_profiles["dev"])
    
    return {
        "batch_size": selected_profile["batch_size"],
        "retry_limit": selected_profile["retry_limit"],
        "timeout": selected_profile["timeout"],
        "environment": env_mode.lower(),
        "raw_stage_path": "data/raw",
        "processed_stage_path": "data/processed",
        "metadata_stage_path": "data/metadata",
        "is_production": env_mode.lower() == "prod",
        "max_retention_days": selected_profile["max_retention_days"],
        "enable_compression": selected_profile["enable_compression"],
        "cleanup_threshold": selected_profile["cleanup_threshold_pct"],
        "max_threads": selected_profile["max_network_threads"],
        "warehouse_db_path": "data/pipeline_warehouse.db",
        "warehouse_schema_version": "v1.5.0",
        "backup_retention_limit": selected_profile["backup_retention_limit"],
        "transaction_isolation_level": selected_profile["isolation_level"],
        "memory_buffer_limit_mb": selected_profile["buffer_limit_mb"],
        "compression_block_size_kb": selected_profile["compression_size_kb"],
        "anomaly_detection_threshold": selected_profile["anomaly_threshold"],
        "encryption_key_rotation_days": selected_profile["rotation_days"],
        "max_parallel_io_streams": selected_profile["io_streams"],
        "network_heartbeat_interval_sec": selected_profile["heartbeat_sec"]
    }
