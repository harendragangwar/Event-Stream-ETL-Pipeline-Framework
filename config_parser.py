import json

def load_pipeline_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            print("Configuration loaded successfully")
            return config
    except FileNotFoundError:
        print("Config file not found, loading defaults")
        return {"batch_size": 100, "retry_count": 3}

if __name__ == "__main__":
    load_pipeline_config("config.json")
