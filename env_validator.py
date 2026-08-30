import os
import sys

def verify_required_env_vars():
    required_vars = ["DB_HOST", "DB_USER", "DB_PASS"]
    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {missing_vars}")
        return False
    print("required environment configurations are verified")
    return True

if __name__ == "__main__":
    verify_required_env_vars()
