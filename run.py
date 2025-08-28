import json
import time
from bank_adapter_factory import BankAdapterFactory
from utils.driver_init import ensure_app_installed, init_driver, grant_post_notification_permission
from utils.device_utils import uninstall_app, is_app_installed, launch_app_once, restart_app

# ✅ Chỉ cần đổi dòng này là chạy bank khác
BANK_NAME = "SHBank"
USER_ID = "SHB280802"

def load_config(bank_name):
    config_path = f"configs/{bank_name.lower()}_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    config["bank_name"] = bank_name  # Chỉ gán bank_name để tránh nhầm
    return config

# def prepare_driver(config):
#     ensure_app_installed(config["apk_v1_path"], config["desired_caps"]["appPackage"])
#     launch_app_once(config["desired_caps"]["appPackage"])
#     return init_driver(config["desired_caps"], config["timeout"])

def prepare_driver(config):
    package_name = config["desired_caps"]["appPackage"]

    # Gỡ cài đặt ứng dụng nếu đã cài
    if is_app_installed(package_name):
        uninstall_app(package_name)
        print(f"[INFO] Đã gỡ cài đặt ứng dụng: {package_name}")

    # Cài đặt lại ứng dụng
    ensure_app_installed(config["apk_v2_path"], package_name)
    print(f"[INFO] Đã cài đặt lại ứng dụng từ: {config['apk_v2_path']}")

    # Mở ứng dụng lần đầu
    launch_app_once(package_name)

    # Khởi tạo driver
    return init_driver(config["desired_caps"], config["timeout"])

def main():
    config = load_config(BANK_NAME)

    for i in range(100):
        print(f"\n🔁 [{BANK_NAME}] Lần chạy thứ {i+1}")

        driver = prepare_driver(config)
        config["driver"] = driver

        package_name = config["desired_caps"]["appPackage"]
        grant_post_notification_permission(package_name)

        adapter = BankAdapterFactory.create_adapter(BANK_NAME, config)

        # 👉 Chạy luồng mong muốn
        #Luồng login
        # adapter.dispatch_flow("login",USER_ID)
        # restart_app(driver,config["desired_caps"]["appPackage"])

        #Luồng kích hoạt
        adapter.dispatch_flow("register",USER_ID)

        # Luồng nâng cấp
        # adapter.test_upgrade_flow(USER_ID)

        #👉 Gỡ app sau khi test
        if is_app_installed(package_name):
            uninstall_app(package_name)
            print(f"🗑️ Đã gỡ cài đặt ứng dụng: {package_name}")
        else:
            print(f"ℹ️ App chưa được cài: {package_name}")

        driver.quit()

if __name__ == "__main__":
    main()
