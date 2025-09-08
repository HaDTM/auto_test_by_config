import json
import re
from unicodedata import digit
import requests
import time
from requests.auth import HTTPBasicAuth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.device_utils import restart_app, update_app

from payloads.build_activation_payload import build_activation_payload
from payloads.build_payload_otp import build_otp_payload, build_otpcr_payload
from payloads.build_payload_transaction import build_create_transaction_payload, call_api_create_transaction,build_headers, generate_transaction_id_uuid
from selenium.common.exceptions import StaleElementReferenceException



class VTBAdapter:
    def __init__(self, config):
        self.config = config
        self.driver = config["driver"]
        caps = config["desired_caps"]
        self.timeout = config["timeout"]

    def activate(self, user_id):
        print(f"[INFO] UserID hiện tại: {user_id}")
        self._click(self.config["element_ids"]["intro_vi_lang"])

        self._click(self.config["element_ids"]["term_btnAgree"])

        activation_code = self._fetch_activation_code(user_id)
        if not activation_code:
            print("[ERROR] Không lấy được mã kích hoạt.")
            return  # Dừng lại, không nhập mã và không đặt PIN
        time.sleep(3)
        print(f"[INFO] Nhập mã kích hoạt: {activation_code}")
        self._input_activation_code(activation_code)

        self._click(self.config["element_ids"]["active_btnActive"])

        # Nếu cần: chờ confirm popup hoặc next screen rồi mới đặt PIN
        # WebDriverWait(self.driver, self.timeout).until(
        #     EC.presence_of_element_located((By.ID, self.config["element_ids"]["pin_screen_id"]))
        # )
        
    def enter_pin(self,pin_code):
        print(f"[INFO] Nhập PIN: {pin_code}")
        for digit in pin_code:
            self._click_xpath(self.config["element_ids"]["number_pin_button_xpath"], digit)

    def confirm_pin(self):
        self._click(self.config["element_ids"]["set_pin_button"])

    def _fetch_activation_code(self, user_id):
        payload = build_activation_payload(self.config, user_id)
        url = self.config["activation_code_url"]
        headers = build_headers(self.config)
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("activationCode")
        except Exception as e:
            print(f"[ERROR] Gọi API kích hoạt thất bại: {e}")
            return None


    def _input_activation_code(self, activation_code):
        for digit in activation_code:
            self._click_xpath(self.config["element_ids"]["number_pin_button_xpath"], digit)

    def choose_to_basic(self):
        self._click(self.config["element_ids"]["user_name_button"])
        time.sleep(2)
        self._click(self.config["element_ids"]["basic_tab_button"])
    
    def choose_to_advance(self):
        self._click(self.config["element_ids"]["user_name_button"])

    def get_otp_from_app(self):
        print("[INFO] Đang lấy OTP từ giao diện app...")
        raw_otp = self._get_element_text(self.config["element_ids"]["otp_show"])
        print(f"[INFO] OTP nguyên bản: '{raw_otp}'")
        otp_value = self._clean_otp(raw_otp)
        print(f"[INFO] OTP sau xử lý: '{otp_value}'")
        return otp_value
    
    def _clean_otp(self, raw_otp):
        if not raw_otp:
            return None
        cleaned = re.sub(r"\s+", "", raw_otp).strip()
        if cleaned.isdigit() and len(cleaned) == 6:
            return cleaned
        print(f"[WARN] OTP không đúng định dạng: '{cleaned}'")
        return 

    def verify_otp(self, type, user_id, otp_input, transaction_id):
        try:
            if type == "basic":
                url = self.config["otp_basic_url"]
                payload = build_otp_payload( self.config, user_id, otp_input, transaction_id)
            elif type == "cr":
                url = self.config["otp_advance_url"]
                payload = build_otpcr_payload( self.config,user_id, otp_input, transaction_id)
            else:
                raise ValueError("Loại OTP không hợp lệ.")
            
            headers = build_headers(self.config)
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout, verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Xác thực OTP thất bại: {e}")
            return {}

    def create_transaction(self, user_id):
        return call_api_create_transaction(self.config, user_id)

    def sync_otp(self):
        self._click(self.config["element_ids"]["setting_button"])
        self._click(self.config["element_ids"]["sync_time_button"])
        self._click(self.config["element_ids"]["sync_button"])
        time.sleep(2)
        print("[INFO] Đã click vào nút 'Đồng bộ OTP'.")

    def add_new_user(self):
        # Click vào nút "Thêm người dùng"
        self._click(self.config["element_ids"]["edit_user_button"])

        self._click(self.config["element_ids"]["add_user_button"])
        print("[INFO] Đã click vào nút 'Thêm người dùng'.")

        # Gọi hàm activate với user_id là "NewUser"
        user_id = "NewUser"
        print(f"[INFO] UserID hiện tại: {user_id}")

        activation_code = self._fetch_activation_code(user_id)
        if not activation_code:
            print("[ERROR] Không lấy được mã kích hoạt.")
            return  # Dừng lại, không nhập mã và không đặt PIN
        time.sleep(3)

        print(f"[INFO] Nhập mã kích hoạt: {activation_code} cho {user_id}")

        self._input_activation_code(activation_code)
        print(f"[INFO] Người dùng mới {user_id} đã được thêm thành công.")

    def activation_flow(self, user_id):
        self.activate(user_id)

        pin = self.config.get("setPIN")
        self.enter_pin(pin)
        self.enter_pin(pin)

        self._click(self.config["element_ids"]["finger_btnSkip"])

        time.sleep(3)
        # self._click(self.config["element_ids"]["back_button"])
        
        transaction_id = self.create_transaction(user_id)

        self.choose_to_advance()

        self._click(self.config["element_ids"]["error_message"])
        
        self._click(self.config["element_ids"]["get_transaction_button"])

        self._click(self.config["element_ids"]["sign_transaction"])

        otp_cr = self.get_otp_from_app()
        print(f"[DEBUG] Transaction ID để xác thực nâng cao: {transaction_id}")
        result_cr = self.verify_otp("cr", user_id, otp_cr, transaction_id)
        print(f"[RESULT] Xác thực OTP nâng cao: {result_cr}")

        status = self.sync_otp()
        print(f"Tình trạng đồng bộ: {status}")

        return {
            "otp_advanced": result_cr,
            "transaction_id": transaction_id
        }

    def login_flow(self, user_id):

        pin = self.config.get("setPIN")
        self.enter_pin(pin)
        self._click(self.config["element_ids"]["login_btnConfirm"])
        print("Login với pin")
        time.sleep(3)
        
        self._click(self.config["element_ids"]["back_button"])

        transaction_id = self.create_transaction(user_id)
        self.choose_to_advance()
        
        # self._click(self.config["element_ids"]["get_transaction_button"])

        self._click(self.config["element_ids"]["sign_transaction"])

        otp_cr = self.get_otp_from_app()
        print(f"[DEBUG] Transaction ID để xác thực nâng cao: {transaction_id}")
        result_cr = self.verify_otp("cr", user_id, otp_cr, transaction_id)
        print(f"[RESULT] Xác thực OTP nâng cao: {result_cr}")

        status = self.sync_otp()
        print(f"Tình trạng đồng bộ: {status}")

        return {
            "otp_advanced": result_cr,
            "transaction_id": transaction_id
        }

    def add_user_flow(self, user_id):
        pin = self.config.get("setPIN")
        self.enter_pin(pin)
        self._click(self.config["element_ids"]["login_btnConfirm"])
        print("Login với pin")
        time.sleep(3)

        # Add new user
        self.add_new_user()
        return {"status": "New user added"}

    def dispatch_flow(self, screen_name, user_id):
        routes = {
            "login": self.login_flow,
            "register": self.activation_flow,
            "update": self.test_upgrade_flow,
            "adduser": self.add_user_flow
            # có thể mở rộng: "update": self.update_user_info
        }
        if screen_name in routes:
            print(f"[INFO] Bắt đầu luồng: {screen_name}")
            return routes[screen_name](user_id)
        else:
            print(f"[WARN] Màn hình '{screen_name}' chưa có luồng xử lý.")
            return None
        
# Hàm custom -> pending khi có yêu cầu nhé, lười vãi ò
    def post_login_menu(self, user_id):
        test_actions = [
            ("Xác thực OTP thường", self.verify_otp),
            ("Xác thực OTP nâng cao", self.verify_otp_cr),
            ("Đồng bộ OTP", self.sync_otp)
        ]

        while True:
            print("\n📋 Danh sách lệnh test:")
            for i, (desc, _) in enumerate(test_actions, start=1):
                print(f"{i}. {desc}")

            cmd = input("\nNhập số để test (hoặc '0' để thoát): ").strip()

            if cmd == "0":
                print("🛑 Kết thúc test.")
                break
            elif cmd.isdigit() and 1 <= int(cmd) <= len(test_actions):
                idx = int(cmd) - 1
                print(f"🔧 Đang gọi: {test_actions[idx][0]}")
                test_actions[idx][1](user_id)
            else:
                print("❌ Số không hợp lệ. Nhập lại hộ cái.")

# Hàm restart app, có thể dùng trong các trường hợp cần thiết
    def restart_app_from_config(self):
        app_package = self.config["desired_caps"]["appPackage"]
        restart_app(self.driver, app_package)

    def test_upgrade_flow(self, user_id):
        try:
            # Cập nhật ứng dụng lên phiên bản 1
            print(f"[INFO] Đang cập nhật ứng dụng lên phiên bản 1 từ: {self.config['apk_v1_path']}")
            update_app(self.config["apk_v1_path"])
            print("[INFO] Cập nhật ứng dụng phiên bản 1 thành công.")

            # Khởi động lại ứng dụng phiên bản 1
            print("[INFO] Đang khởi động lại ứng dụng phiên bản 1...")
            restart_app(self.driver, self.config["desired_caps"]["appPackage"])
            print("[INFO] Ứng dụng phiên bản 1 đã được khởi động lại.")

            # Thực hiện luồng "register" trên phiên bản 1
            print("[INFO] Bắt đầu luồng 'register' trên phiên bản 1.")
            self.dispatch_flow("register", user_id)

            # Cập nhật ứng dụng lên phiên bản 2
            print(f"[INFO] Đang cập nhật ứng dụng lên phiên bản 2 từ: {self.config['apk_v2_path']}")
            update_app(self.config["apk_v2_path"])
            print("[INFO] Cập nhật ứng dụng phiên bản 2 thành công.")

            # Khởi động lại ứng dụng phiên bản 2
            print("[INFO] Đang khởi động lại ứng dụng phiên bản 2...")
            restart_app(self.driver, self.config["desired_caps"]["appPackage"])
            print("[INFO] Ứng dụng phiên bản 2 đã được khởi động lại.")

            # Thực hiện luồng "login" trên phiên bản 2
            print("[INFO] Bắt đầu luồng 'login' trên phiên bản 2.")
            self.dispatch_flow("login", user_id)

        except Exception as e:
            print(f"[ERROR] Lỗi trong quá trình kiểm thử nâng cấp ứng dụng: {e}")
            # Optional: Chụp màn hình để debug
            self.driver.save_screenshot(f"error_upgrade_flow_{int(time.time())}.png")
            raise

    # 👇 Các hàm tương tác UI thật sự bằng Appium + wait

    def _click(self, element_id):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            element.click()
        except StaleElementReferenceException:
            print("⚠️ Element bị stale, đang thử lại...")
            time.sleep(1)
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            element.click()


    def _click_xpath(self, xpath_template, digit, timeout=None):
            timeout = timeout or self.timeout
            try:
                xpath = xpath_template.format(digit=digit)
                print(f"[DEBUG] Đang tìm và click vào xpath: {xpath}")
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                element.click()
                print(f"[INFO] Đã click vào số PIN: {digit}")
            except Exception as e:
                print(f"❌ Không click được vào số PIN '{digit}' với xpath '{xpath}' → {e}")
                # Optional: chụp màn hình để debug
                self.driver.save_screenshot(f"error_click_pin_{digit}_{int(time.time())}.png")

    def _set_element_text(self, element_id, text):
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        ).send_keys(text)

    def _get_element_text(self, element_id, by=By.ID, timeout=None):
        timeout = timeout or self.timeout
        try:
            print(f"[DEBUG] Đang tìm element: {element_id} bằng {by}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, element_id))
            )
            text = element.text
            print(f"[INFO] Text lấy được từ element '{element_id}': {text}")
            return text
        except Exception as e:
            print(f"❌ Không lấy được text từ element '{element_id}' → {e}")
            return None