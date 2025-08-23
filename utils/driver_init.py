import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import subprocess

def ensure_app_installed(apk_path, package_name):
    result = os.popen("adb shell pm list packages").read()
    if package_name not in result:
        print(f"[INFO] App chưa cài. Tiến hành cài lại từ: {apk_path}")
        os.system(f"adb install {apk_path}")
    else:
        print(f"[INFO] App đã cài sẵn: {package_name}")

#Cái này để sau này mình viết nhé, giờ mình lười lắm.
def get_connected_device_info():
    # Lấy danh sách thiết bị
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    devices = [line.split()[0] for line in lines[1:] if "device" in line]

    if not devices:
        print("❌ Không có thiết bị nào đang kết nối.")
        return None

    device_id = devices[0]  # Lấy thiết bị đầu tiên
    def get_prop(prop):
        res = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", prop],
            capture_output=True, text=True
        )
        return res.stdout.strip()

    info = {
        "device_id": device_id,
        "model": get_prop("ro.product.model"),
        "manufacturer": get_prop("ro.product.manufacturer"),
        "android_version": get_prop("ro.build.version.release"),
        "sdk": get_prop("ro.build.version.sdk")
    }

    print(f"📱 Thiết bị đang kết nối: {info}")
    return info

def grant_post_notification_permission(package_name):
    # Lấy SDK version
    result = subprocess.run(
        ["adb", "shell", "getprop", "ro.build.version.sdk"],
        capture_output=True, text=True
    )
    sdk_version = int(result.stdout.strip())

    # Nếu Android 13 trở lên (SDK >= 33), thì cấp quyền
    if sdk_version >= 33:
        subprocess.run([
            "adb", "shell", "pm", "grant",
            package_name, "android.permission.POST_NOTIFICATIONS"
        ])
        print(f"✅ Đã cấp quyền POST_NOTIFICATIONS cho {package_name}")
    else:
        print(f"ℹ️ Thiết bị Android {sdk_version} không cần quyền POST_NOTIFICATIONS")

def init_driver(desired_caps, timeout):
    options = UiAutomator2Options()
    for key, value in desired_caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote("http://localhost:4723", options=options)
     # 👇 In ra activity hiện tại sau khi app được mở
    print("[DEBUG] Activity đang dùng:", driver.current_activity)
    driver.implicitly_wait(timeout)
    return driver
