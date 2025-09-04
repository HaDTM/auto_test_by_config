import json
import os

def load_config(bank_name):
    config_path = f"configs/{bank_name.lower()}_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Không tìm thấy file cấu hình: {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    # Kiểm tra các trường bắt buộc
    required_fields = ["desired_caps", "setPIN"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"❌ Thiếu trường '{field}' trong file cấu hình: {config_path}")

    return config