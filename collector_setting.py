import os
import time
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 이동해야 하는 경우 등 키입력시 사용

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def driver_set():
    options = Options()
    # options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080") # for chrome
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")    
    # options.add_argument("--no-sandbox")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #### chrome #####
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # chrome_driver = "C:\\Python\\chromedriver.exe" # Windows Chrome Driver path
    # chrome_driver = "/usr/local/bin/chromedriver" # Mac Chrome Driver path
    # driver = webdriver.Chrome(chrome_driver, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # # cmd : cd C:\Program Files\Google\Chrome\Application 
    # # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTemp"
    # mac: sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
    # http://localhost:9222/ 접속되는지 확인
    
    driver.set_window_position(2560, 0) # for imac dual monior
    # driver.set_window_position(3520, 0) # for imac dual monior

    driver.implicitly_wait(30)
    return driver

def get_url_untill_done(driver_var, url):
    count = 1
    for i in range(1, 6): # limit trying
        try:
            # 시간 바꾸지마라.. 밴당해 디도스로
            time.sleep(random.uniform(2,3)) # prevent to restrict
            driver_var.get(url)
            time.sleep(random.uniform(2,3))
            print(url + " << " + str(count) + " time try, success!") #, end=""
            break
        except Exception as e:
            # driver_var.implicitly_wait(5)
            print(str(e) + " << " + url + " << " + str(count) + " time try, failed!")
            # time.sleep(3) # without headless
            count+=1
            if i == 5:
                raise
            continue     

def find_date(item_date_temp : str, end_comment, day_keyword, daylist_more=[]): # , day_keyword=False "요일" 있으면 True
    item_date_temp = item_date_temp.replace(" ","") 
    daylist = ["월", "화", "수", "목", "금", "토", "일"]
    first_append = True
    item_date = ""
    
    if len(daylist_more) != 0:
        daylist = daylist_more + daylist
    if item_date_temp.find(end_comment) != -1: # end_comment = 완료?
        item_date = "완결"
        item_finish_status = "완결"
    else:
        item_finish_status = "연재"
        for d in daylist:
            if item_date_temp.find(d) != -1:
                if d == "일" and day_keyword == True and item_date_temp.find("일요일") == -1:
                    break                    
                if first_append == True:
                    item_date += d
                    first_append = False
                else:                    
                    item_date += "," + d
    return item_date, item_finish_status              


def login_for_adult(driver, user_id, user_pw, id_tag, pw_tag):
    driver.find_element(By.XPATH, id_tag).send_keys(user_id)
    time.sleep(random.uniform(1, 2))
    driver.find_element(By.XPATH, pw_tag).send_keys(user_pw)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(Keys.ENTER)
    time.sleep(random.uniform(2,3))

def is_adult(item_adult_string, key_word):
    if item_adult_string.find(key_word) != -1: # adult
        return True
    else:
        return False
    
        
    
"""
파이썬 웹툰데이타 클래스를 만들까? 만들어서 instance 로 id, title.. 저장하는게 더 빠르거나 깔끔하려나? 
getId 같은 함수만들어서 해도되고.. 지금은 리스트의 순서에 의존해서 구분하고 있으니까 클래스만드는게 깔끔할듯하다
"""

class webtoon_data:
    def __init__(self):
        pass