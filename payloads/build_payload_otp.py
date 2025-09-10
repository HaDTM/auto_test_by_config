import json


def build_otp_payload(config, user_id, otp, transaction_id):
    return {
        "issuerName": config.get("issuer_name", "HDBank"),
        "userID": user_id,
        "otp": "00" + otp,
        "transactionID": transaction_id
    }
    

def build_otpcr_payload(config, user_id, otp, transaction_id):
    if config.get("payload_file"):
        # Đọc payload từ file
        with open(config["payload_file"], "r", encoding="utf-8") as f:
            payload_template = json.load(f)
        payload = payload_template["otp"]  # Lấy payload từ trường "otp" trong file

        # Thay thế các placeholder trong payload
        payload["otp"] = f"04{otp}"
        payload["userID"] = payload["userID"].replace("{user_id}", user_id)
        payload["transactionID"] = payload["transactionID"].replace("{transaction_id}", transaction_id)
    else:
        # Logic mặc định nếu không có file payload
        payload = {
            "issuerName": config["issuer_name"],  # Lấy từ config
            "userID": user_id,
            "otp": f"09{otp}",
            "transactionID": transaction_id
        }
    return payload
