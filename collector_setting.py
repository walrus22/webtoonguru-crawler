from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys # 이동해야 하는 경우 등 키입력시 사용
from webdriver_manager.chrome import ChromeDriverManager

def driver_set():
    options = Options()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(300)
    return driver
