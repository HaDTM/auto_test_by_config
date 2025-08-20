# 📂 run.py

import json
from bank_adapter_factory import BankAdapterFactory
from utils.driver_init import init_driver

# def main():
#     USER_ID = "280701"

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

    
#     adapter.dispatch_flow("login", USER_ID)


def main():
    USER_ID = "280701"

    # Load config
    with open("configs/hdbank_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    for i in range(500):
        print(f"\n🔁 Lần chạy thứ {i+1}")

        # Init driver mỗi lần để app tự mở lại
        driver = init_driver(config["desired_caps"], config["timeout"])
        config["driver"] = driver

        # Tạo adapter qua factory
        adapter = BankAdapterFactory.create_adapter("HDBank", config)

        # Chạy luồng mong muốn
        adapter.dispatch_flow("login", USER_ID)
        adapter.restart_app()

        # Đóng app sau khi chạy xong
        driver.quit()




if __name__ == "__main__":
    main()
