import requests
import json
import urllib3

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://192.168.0.112:8445/keypass.ws.tpb/getActivationCode"

payload = {
    "issuerName": "Keypass",
    "userID": "0001",
    "aidVersion": "99",
    "userName": "0001",
    "cifNumber": "234567890123456789",
    "phoneNumber": "0903123321",
    "branchID": "001",
    "email": "test01@gmail.com.vn",
    "customerTypeID": 2,
    "customerName": "Tap Doan MK",
    "mobileAppId": 2,
    "channelId": 2,
    "userType": "1"
}

headers = {
    "Content-Type": "application/json",
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