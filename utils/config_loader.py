import json
import os

def load_config(bank_name):
    config_path = f"configs/{bank_name.lower()}_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    config["bank_name"] = bank_name  # Chỉ gán bank_name để tránh nhầm
    return config