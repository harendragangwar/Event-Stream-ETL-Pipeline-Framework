import os

def initialize_landing_zone(directories):
    for folder in directories:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created landing zone directory: {folder}")
        else:
            print(f"Directory already exists: {folder}")

if __name__ == "__main__":
    zones = ["data/raw", "data/processed", "data/logs"]
    initialize_landing_zone(zones)
