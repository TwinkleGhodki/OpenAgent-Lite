# browser_manager.py

from selenium import webdriver

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = webdriver.Chrome()
    return _driver

def close_driver():
    global _driver
    if _driver is not None:
        _driver.quit()
        _driver = None
