import os
def get_pipeline_settings():
    env_mode = os.getenv("PIPELINE_ENV", "dev")
    return {
        "batch_size": 500,
        "retry_limit": 3,
        "timeout": 30,
        "environment": env_mode,
        "raw_stage_path": "data/raw",
        "processed_stage_path": "data/processed",
        "is_production": env_mode.lower() == "prod"
    }
