import os
import time
import subprocess

def install_apk(apk_path):
    full_path = os.path.abspath(apk_path)
    print(f"📦 Installing APK from: {full_path}")
    subprocess.run(["adb", "install", "-r", full_path], check=True)

def update_app(apk_path):
    try:
        print(f"📦 Updating app with APK: {apk_path}")
        subprocess.run(["adb", "install", "-r", apk_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi update app: {e}")

def restart_app(driver, package_name):
    try:
        driver.terminate_app(package_name)
        time.sleep(1)
        driver.activate_app(package_name)
    except Exception as e:
        print(f"❌ Lỗi khi restart app: {e}")
