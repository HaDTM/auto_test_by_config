import json


def build_otp_payload(config, user_id, otp, transaction_id):
    return {
        "issuerName": config.get("issuer_name", "HDBank"),
        "userID": user_id,
        "otp": "00" + otp,
        "transactionID": transaction_id
    }
    

def build_otpcr_payload(config, user_id, otp, transaction_id):
    # Xác định tiền tố OTP dựa trên bank_name
    bank_name = config.get("issuer_name", "").lower()
    otp_prefix = "04" if bank_name == "vibank" else "09"

    if config.get("payload_file"):
        # Đọc payload từ file
        with open(config["payload_file"], "r", encoding="utf-8") as f:
            payload_template = json.load(f)
        payload = payload_template["otpcr"]  # Lấy payload từ trường "otpcr" trong file

        # Thay thế các placeholder trong payload
        payload["otp"] = f"{otp_prefix}{otp}"
        payload["userID"] = payload["userID"].replace("{user_id}", user_id)
        payload["transactionID"] = payload["transactionID"].replace("{transaction_id}", transaction_id)
    else:
        # Logic mặc định nếu không có file payload
        payload = {
            "issuerName": config["issuer_name"],  # Lấy từ config
            "userID": user_id,
            "otp": f"{otp_prefix}{otp}",
            "transactionID": transaction_id
        }
    return payload
