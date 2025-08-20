from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait


def init_driver(desired_caps, timeout):
    options = UiAutomator2Options()
    for key, value in desired_caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote("http://localhost:4723", options=options)
    driver.implicitly_wait(timeout)
    return driver
