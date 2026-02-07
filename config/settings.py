import os
def get_pipeline_settings():
    env_mode = os.getenv("PIPELINE_ENV", "dev")
    return {
        "batch_size": 500,
        "retry_limit": 3,
        "timeout": 45,
        "environment": env_mode,
        "raw_stage_path": "data/raw",
        "processed_stage_path": "data/processed",
        "metadata_stage_path": "data/metadata",
        "is_production": env_mode.lower() == "prod",
        "max_retention_days": 7
    }
