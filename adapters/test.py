import requests
import json
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TLSAdapter(HTTPAdapter):
    """Adapter để buộc sử dụng một phiên bản TLS cụ thể."""
    def __init__(self, tls_version=None, **kwargs):
        self.tls_version = tls_version
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        kwargs['ssl_version'] = self.tls_version
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, **kwargs)

# Buộc sử dụng TLS 1.2
session = requests.Session()
session.mount("https://", TLSAdapter(ssl.PROTOCOL_TLSv1_2))

url = "https://192.168.0.112:8445/keypass.ws.tpb/createTransaction"

payload = {
  "issuerName": "Keypass",
  "userID": "080901TPBB",
  "transactionID": "080901TPBB",
  "transactionTypeID": 1,
  "transactionData": "080901TPBB|500.50#$|03669839202",
  "isOnline": 0,
  "isPush": 0,
  "notification": {
    "title": "Test_title",
    "body": "Test_body"
  },
  "eSignerTypeID": 3
}

headers = {
    "Content-Type": "application/json",
}

try:
    print("[INFO] Gửi yêu cầu POST đến server...")
    response = session.post(url, headers=headers, data=json.dumps(payload), timeout=20, verify=False)
    if response.status_code == 200:
        print("[SUCCESS] Phản hồi từ server:")
        print(response.text)
    else:
        print(f"[ERROR] Mã lỗi HTTP: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"[ERROR] Lỗi khi gửi yêu cầu: {e}")