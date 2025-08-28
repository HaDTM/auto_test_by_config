import requests
import json
import base64

url = "https://192.168.0.117:8414/keypass.ws/getActivationCode" 

payload = {
    "issuerName": "Keypass",
    "userID": "HADTMTEST",
    "userName": "HADTMTEST",
    "customerName": "HADTMTEST",
    "customerTypeID": 1,
    "cifNumber": "0000000000000002",
    "phoneNumber": "0398448844",
    "email": "test1001@gmail.com",
    "branchID": "001",
    "aidVersion": "99"
}

# auth = base64.b64encode(b"user1:p@ssw0rd#2025").decode("utf-8")
headers = {
    "Content-Type": "application/json",
    # "Authorization": f"Basic {auth}"
}

try:
    print("[INFO] Gửi yêu cầu POST đến server...")
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20, verify=False)
    if response.status_code == 200:
        print("[SUCCESS] Phản hồi từ server:")
        print(response.text)
    else:
        print(f"[ERROR] Mã lỗi HTTP: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"[ERROR] Lỗi khi gửi yêu cầu: {e}")

