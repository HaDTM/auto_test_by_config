import json
import time
import os
import argparse
from dotenv import load_dotenv

from bank_adapter_factory import BankAdapterFactory
from utils.driver_init import ensure_app_installed, init_driver, grant_post_notification_permission
from utils.device_utils import uninstall_app, is_app_installed, launch_app_once, restart_app

# Load biến môi trường từ .env
load_dotenv()
BANK_NAME = os.getenv("BANK_NAME")
USER_ID = os.getenv("USER_ID")
LOOP_COUNT = int(os.getenv("LOOP_COUNT", "1"))  # Default = 1 nếu chưa set
DEVICE_NAME = os.getenv("DEVICE_NAME")

if not DEVICE_NAME or not BANK_NAME or not USER_ID:
    raise ValueError("❌ Thiếu giá trị 'DEVICE_NAME' hoặc 'APP_ACTIVITY' hoặc 'BANK_NAME' hoặc 'USER_ID' trong file .env!")

def load_config(bank_name):
    config_path = f"configs/{bank_name.lower()}_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    config["bank_name"] = bank_name

    # Ghi đè giá trị từ .env vào cấu hình
    config["desired_caps"]["deviceName"] = DEVICE_NAME
    print(f"[INFO] Đã ghi đè deviceName: {DEVICE_NAME}")
    print(f"[INFO] appActivity: {config['desired_caps']['appActivity']}")

    return config

def prepare_driver(config, flow):
    package_name = config["desired_caps"]["appPackage"]

    # Chỉ gỡ cài đặt ứng dụng nếu luồng là "update" hoặc "register"
    if flow in ["update", "register"]:
        if is_app_installed(package_name):
            uninstall_app(package_name)
            print(f"[INFO] Đã gỡ cài đặt ứng dụng: {package_name}")

    # Cài đặt ứng dụng tùy theo luồng kiểm thử
    if flow == "update":
        ensure_app_installed(config["apk_v1_path"], package_name)
        print(f"[INFO] Đã cài đặt ứng dụng phiên bản 1 từ: {config['apk_v1_path']}")
    elif flow in ["register", "login", "adduser"]:
        ensure_app_installed(config["apk_v2_path"], package_name)
        print(f"[INFO] Đã cài đặt ứng dụng phiên bản 2 từ: {config['apk_v2_path']}")

    # Mở ứng dụng lần đầu
    launch_app_once(package_name)

    # Khởi tạo driver
    return init_driver(config["desired_caps"], config["timeout"])

def main():
    # Parse tham số từ command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--flow", required=True, choices=["login", "register", "update", "adduser"])
    parser.add_argument("--apk_v2_path", required=False)
    args = parser.parse_args()

    config = load_config(BANK_NAME)

    for i in range(LOOP_COUNT):
        print(f"\n🔁 [{BANK_NAME}] Lần chạy thứ {i+1} ({args.flow})")

        # Chuẩn bị driver và cài đặt ứng dụng theo luồng kiểm thử
        driver = prepare_driver(config, args.flow)
        config["driver"] = driver

        package_name = config["desired_caps"]["appPackage"]
        grant_post_notification_permission(package_name)

        # Khởi động lại ứng dụng nếu cần (chỉ áp dụng cho luồng login)
        if args.flow == "login":
            restart_app(driver, package_name)
            print(f"[INFO] Đã khởi động lại ứng dụng: {package_name}")

        adapter = BankAdapterFactory.create_adapter(BANK_NAME, config)

        # Chọn luồng theo tham số --flow
        if args.flow == "login":
            adapter.dispatch_flow("login", USER_ID)
        elif args.flow == "register":
            adapter.dispatch_flow("register", USER_ID)
        elif args.flow == "update":
            adapter.test_upgrade_flow(USER_ID)
        elif args.flow == "adduser":
            adapter.add_user_flow(USER_ID)

        # Gỡ app sau khi test (chỉ áp dụng cho các luồng cần thiết)
        if args.flow in ["update", "register"] and is_app_installed(package_name):
            uninstall_app(package_name)
            print(f"🗑️ Đã gỡ cài đặt ứng dụng: {package_name}")
        else:
            print(f"ℹ️ Không cần gỡ ứng dụng trong luồng '{args.flow}'.")

        # Đảm bảo ứng dụng được tắt hoàn toàn sau mỗi lần chạy
        if driver:
            try:
                driver.terminate_app(package_name)  # Tắt ứng dụng
                print(f"[INFO] Đã tắt ứng dụng: {package_name}")
            except Exception as e:
                print(f"[WARNING] Không thể tắt ứng dụng: {e}")

        driver.quit()

if __name__ == "__main__":
    main()