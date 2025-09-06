import uuid
import requests
import base64
import json

def generate_transaction_id_uuid():
    return str(uuid.uuid4())

def build_create_transaction_payload(user_id, transaction_id, config):
    if config.get("payload_file"):
        with open(config["payload_file"], "r", encoding="utf-8") as f:
            payload_template = json.load(f)
        payload = payload_template["create_transaction"]

        # Thay thế các placeholder trong payload
        payload["userID"] = user_id
        payload["transactionID"] = transaction_id
        if "{transaction_id}" in payload["transactionData"]:
            payload["transactionData"] = payload["transactionData"].replace("{transaction_id}", transaction_id)
    else:
        # Logic mặc định cho các ngân hàng khác
        payload = {
            "issuerName": config.get("issuer_name", "DefaultBank"),
            "userID": user_id,
            "transactionID": transaction_id,
            "transactionTypeID": 10,
            "transactionData": f"{transaction_id}|818794922918113218389848863|TRAN THI THANH KIEU - 1234567890123456789|1585456000|VND",
            "challenge": "",
            "callbackUrl": "",
            "isOnline": 0,
            "isPush": 0,
            "notification": None,
            "eSignerTypeID": 12,
            "channelID": 0
        }
    return payload

def build_headers(config):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if config.get("requires_basic_auth"):
        user = config["auth_user"]
        password = config["auth_password"]
        auth_string = f"{user}:{password}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        headers["Authorization"] = f"Basic {encoded}"

    # Tùy chỉnh headers cho SHBank
    if config.get("issuer_name") == "SHBank":
        headers["Custom-Header"] = "SHBank-Specific-Value"  # Ví dụ: Thêm header tùy chỉnh cho SHBank

    return headers
#Chỗ này là của thằng getOCRAQuestion
def build_getOCRAQuestion_payload(config, user_id, transaction_id):
    return {
        "issuerName": config.get("issuer_name", "DefaultBank"),
        "userID": user_id,
        "aidVersion": "04",
        "sysChallenge": "",
        "transactionID": transaction_id
    }

def call_api_getOCRAQuestion(config, user_id, transaction_id):
    payload = build_getOCRAQuestion_payload(config, user_id, transaction_id)
    headers = build_headers(config)

    url = config["transaction_url"]
    response = requests.post(url, json=payload, headers=headers, verify=False)
    response.raise_for_status()

    data = response.json()
    print(f"✅ Kết quả getOCRAQuestion:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return data.get("challenge")

def call_api_create_transaction(config, user_id):
    transaction_id = generate_transaction_id_uuid()
    print(f"[DEBUG] Generated transaction_id: {transaction_id}")  # In ra giá trị transaction_id
    payload = build_create_transaction_payload(user_id, transaction_id, config)
    print(f"[DEBUG] Payload gửi lên: {payload}")
    headers = build_headers(config)

    url = config["transaction_url"]
    response = requests.post(url, json=payload, headers=headers, verify=False)
    response.raise_for_status()
    
    data = response.json()
    print(f"✅ Kết quả createTransaction:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return data.get("transactionID")