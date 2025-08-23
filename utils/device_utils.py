import os
import time
import subprocess

def install_apk(apk_path):
    full_path = os.path.abspath(apk_path)
    print(f"📦 Installing APK from: {full_path}")
    subprocess.run(["adb", "install", "-r", full_path], check=True)

def is_app_installed(package_name):
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages", package_name],
            capture_output=True, text=True, check=True
        )
        return package_name in result.stdout
    except subprocess.CalledProcessError:
        return False

def launch_app_once(package_name):
    import subprocess
    print(f"[INFO] Mở app {package_name} lần đầu để khởi tạo")
    cmd = [
        "adb", "shell", "monkey",
        "-p", package_name,
        "-c", "android.intent.category.LAUNCHER",
        "1"
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    print(f"[INFO] App {package_name} đã được mở thành công")

def uninstall_app(package_name):
    try:
        print(f"🗑️ Uninstalling app with package name: {package_name}")
        subprocess.run(["adb", "uninstall", package_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi gỡ cài đặt ứng dụng: {e}")

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
