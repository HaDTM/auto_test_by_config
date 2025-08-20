import uuid
import requests
import base64
import json

def generate_transaction_id_uuid():
    return str(uuid.uuid4())

def build_create_transaction_payload(user_id, transaction_id):
    transaction_data = f"{transaction_id}|818794922918113218389848863|TRAN THI THANH KIEU - 1234567890123456789|1585456000|VND"

    return {
        "issuerName": "HDBank",
        "userID": user_id,
        "transactionID": transaction_id,
        "transactionTypeID": 10,
        "transactionData": transaction_data,
        "challenge": "",
        "callbackUrl": "",
        "isOnline": 0,
        "isPush": 1,
        "notification": {
            "title": "Test_title",
            "body": "Test_body"
        },
        "eSignerTypeID": 12,
        "channelID": 0
    }

def build_headers(config):
    headers = {}
    if config.get("requires_basic_auth"):
        user = config["auth_user"]
        password = config["auth_password"]
        auth_string = f"{user}:{password}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        headers["Authorization"] = f"Basic {encoded}"
    return headers

def call_api_create_transaction(config, user_id):
    transaction_id = generate_transaction_id_uuid()
    payload = build_create_transaction_payload(user_id, transaction_id)
    headers = build_headers(config)

    url = config["transaction_url"]
    response = requests.post(url, json=payload, headers=headers, verify=False)
    response.raise_for_status()

    data = response.json()
    print(f"✅ Kết quả createTransaction:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return data.get("transactionID")
