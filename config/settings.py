import os

def get_pipeline_settings():
    return {
        "batch_size": 500,
        "retry_limit": 3,
        "timeout": 30,
        "environment": os.getenv("PIPELINE_ENV", "development"),
        "raw_stage_path": "data/raw",
        "processed_stage_path": "data/processed"
    }
