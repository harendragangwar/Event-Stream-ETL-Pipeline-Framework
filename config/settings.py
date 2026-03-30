import os

def get_pipeline_settings():
    env_mode = os.getenv("PIPELINE_ENV", "dev")
    config_profiles = {
        "prod": {
            "batch_size": 5000,
            "retry_limit": 5,
            "timeout": 120,
            "max_retention_days": 30
        },
        "dev": {
            "batch_size": 1000,
            "retry_limit": 3,
            "timeout": 45,
            "max_retention_days": 7
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
        "warehouse_db_path": "data/pipeline_warehouse.db"
    }
