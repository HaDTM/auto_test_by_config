import json
import os

def load_config(bank_name):
    file_name = f"{bank_name.lower()}_config.json"
    config_path = os.path.join("configs", file_name)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    config["issuer_name"] = bank_name  # đảm bảo luôn có issuer_name
    return config