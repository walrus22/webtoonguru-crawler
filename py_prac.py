import os
import time
import random
from PIL import Image
from urllib.request import urlopen
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 이동해야 하는 경우 등 키입력시 사용
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

#### chrome #####
# chrome_options = chromeOptions()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_driver = "C:\\Python\\chromedriver.exe" # Your Chrome Driver path
# driver = webdriver.Chrome(chrome_driver, options=chrome_options)
# url = "https://webtoon.kakao.com/ranking"
# driver.get(url)

# # cmd : cd C:\Program Files\Google\Chrome\Application 
# # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTemp"

#### firefox ####
firefox_options = firefoxOptions()
# firefox_options.add_argument("debuggerAddress", "127.0.0.1:6000")
firefox_driver = "C:\\Python\\geckodriver.exe" # Your Chrome Driver path
driver = webdriver.Firefox(service=Service(firefox_driver, service_args=['--marionette-port', '2828', '--connect-existing']), options=firefox_options)
##################

url = "https://webtoon.kakao.com/content/%EA%B2%80%EB%B9%A8%EB%A1%9C-%EB%A0%88%EB%B2%A8%EC%97%85/2922"
# url = "https://webtoon.kakao.com/content/%EC%9D%B4%ED%86%A0%EB%A1%9D-%EB%B3%B4%ED%86%B5%EC%9D%98/1351"
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
print()
driver.get(url)
time.sleep(1)


fore_temp = driver.find_elements(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/*")[0]
if fore_temp.tag_name == "video":
    foreground = Image.open(urlopen(fore_temp.get_attribute("poster"))).convert("RGBA")
    
else :
    foreground = Image.open(urlopen(fore_temp.find_element(By.XPATH, "./img").get_attribute("src"))).convert("RGBA")
    
foreground.show()
    
    
# Image.open(urlopen(driver.find_element(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/picture/source[2]").get_attribute("srcset"))).convert("RGBA")

print((fore_temp.tag_name))
# foreground = Image.open(urlopen(driver.find_element(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/picture/source[2]").get_attribute("srcset"))).convert("RGBA")

# if 


# cmd : cd C:\Program Files\Mozilla Firefox
# firefox.exe -marionette --profile C:\FirefoxTEMP

# # def driver_set():
# #     options = Options()
# #     options.add_argument("--width=1920"); options.add_argument("--height=1080"); #for firefox
# #     options.add_argument
# #     driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
# #     driver.implicitly_wait(300)

# # url = "https://webtoon.kakao.com/ranking"
# # driver = driver_set()
# # get_url_untill_done(driver, url)

# time.sleep(100)

# time.sleep(3)

# item_title = title_temp.text
# item_synopsis = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")
# item_artist = driver.find_element(By.XPATH, "//div[@class='overflow-hidden cursor-pointer']/p[2]").text
# time.sleep(1)
# title_temp.click()
# time.sleep(1)



# print()

# print()