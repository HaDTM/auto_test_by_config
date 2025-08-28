import base64


def build_activation_payload(config, user_id):
    return {
        "issuerName": config["issuer_name"],  # Lấy từ config
        "userID": user_id,
        "userName": f"userName {user_id}",
        "customerName": f"customerName {user_id}",
        "customerTypeID": 1,
        "cifNumber": "0000000000000002",
        "phoneNumber": "0398448844",
        "email": "test1001@gmail.com",
        "branchID": "001",
        "aidVersion": "99"
    }
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
    return headers
