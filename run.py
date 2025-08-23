# 📂 run.py

import json
from bank_adapter_factory import BankAdapterFactory
from utils.driver_init import ensure_app_installed, init_driver, grant_post_notification_permission
from utils.device_utils import uninstall_app, is_app_installed, launch_app_once

# def main():
#     USER_ID = "200801"

#     # Load config
#     with open("configs/hdbank_config.json", "r", encoding="utf-8") as f:
#         config = json.load(f)

#     # Init driver
#     driver = init_driver(config["desired_caps"], config["timeout"])
#     config["driver"] = driver

#     # Tạo adapter qua factory
#     adapter = BankAdapterFactory.create_adapter("HDBank", config)

#     # Chạy luồng mong muốn
#     # adapter.dispatch_flow("register",USER_ID)

    
#     adapter.test_upgrade_flow(USER_ID)

def prepare_driver(config):
    ensure_app_installed(config["apk_v1"], config["desired_caps"]["appPackage"])
    launch_app_once(config["desired_caps"]["appPackage"])
    return init_driver(config["desired_caps"], config["timeout"])


def main():
    USER_ID = "230801"

    # Load config
    with open("configs/hdbank_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    for i in range(100):
        # In ra số lần chạy
        print(f"\n🔁 Lần chạy thứ {i+1}")
        # Đảm bảo APK đã được cài đặt
        ensure_app_installed(config["apk_v1_path"], config["desired_caps"]["appPackage"])
        launch_app_once(config["desired_caps"]["appPackage"])

        # Init driver mỗi lần để app tự mở lại
        driver = init_driver(config["desired_caps"], config["timeout"])
        config["driver"] = driver

        package_name = config["desired_caps"]["appPackage"]
        grant_post_notification_permission(package_name)
        # Tạo adapter qua factory
        adapter = BankAdapterFactory.create_adapter("HDBank", config)

        # Chạy luồng mong muốn

        #Luồng login
        # adapter.dispatch_flow("login", USER_ID)
        # adapter.restart_app()

        # Luồng update app
        adapter.test_upgrade_flow(USER_ID)
        
        # Gỡ app sau khi test upgrade flow
        package_name = config["desired_caps"]["appPackage"]
        if is_app_installed(package_name):
            uninstall_app(package_name)
            print(f"🗑️ Đã gỡ cài đặt ứng dụng: {package_name}")
        else:
            print(f"ℹ️ App chưa được cài: {package_name}")

        # Đóng app sau khi chạy xong
        driver.quit()




if __name__ == "__main__":
    main()
