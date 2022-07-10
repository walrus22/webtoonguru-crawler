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

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager




def driver_set():
    options = Options()
    # options.add_argument("--incognito")
    # options.add_argument("--window-size=1920,1080") # for chrome
    # options.add_argument("--width=1920"); options.add_argument("--height=1080"); #for firefox
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")    
    # options.add_argument("--no-sandbox")
    
    #### chrome #####
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "C:\\Python\\chromedriver.exe" # Your Chrome Driver path
    driver = webdriver.Chrome(chrome_driver, options=options)
    # url = "https://webtoon.kakao.com/ranking"
    # driver.get(url)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # # cmd : cd C:\Program Files\Google\Chrome\Application 
    # # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTemp"

    #### firefox ####
    # options.add_argument("debuggerAddress", "127.0.0.1:6000")
    # firefox_driver = "C:\\Python\\geckodriver.exe" # Your Chrome Driver path
    # url = "https://webtoon.kakao.com/ranking"
    # driver.get(url)

    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing']), options=options)
    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install(), service_args=['--marionette-port', '2828']), options=options)
    # # cmd : cd C:\Program Files\Mozilla Firefox
    # # firefox.exe -marionette --profile C:\FirefoxTEMP
    # # firefox.exe --headless -marionette --profile C:\FirefoxTEMP

    driver.implicitly_wait(300)
    return driver

def get_url_untill_done(driver_var, url):
    count = 1
    for i in range(1, 6): # limit trying
        try:
            # start = time.time()
            time.sleep(random.uniform(2,3)) # prevent to restrict
            # print("sleep :", time.time() - start)   
            driver_var.get(url)
            # start = time.time()
            time.sleep(random.uniform(2,3))
            # print("sleep :", time.time() - start) 
            print(url + " << " + str(count) + " time try, success! ") #, end=""
            
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
    item_date_temp = item_date_temp.replace(" " ,"") 
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
    time.sleep(random.uniform(1,2))
    driver.find_element(By.XPATH, id_tag).send_keys(user_id)
    time.sleep(random.uniform(0.5, 1))
    driver.find_element(By.XPATH, pw_tag).send_keys(user_pw)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(Keys.ENTER)
    time.sleep(random.uniform(3,4))

# def login_for_adult(driver, login_url, login_button_type, login_button_tag, by_type, id_tag = str, pw_tag = str):
#     user_id = "tpa74231@gmail.com"
#     user_pw = "Fortest111!!!"
#     get_url_untill_done(driver, login_url)
#     driver.find_element(login_button_type, login_button_tag).click()
    
#     driver.find_element(by_type, id_tag).send_keys(user_id)
#     driver.find_element(by_type, pw_tag).send_keys(user_pw)
#     time.sleep(3)
#     driver.find_element(by_type, pw_tag).send_keys(Keys.ENTER)
#     time.sleep(3)
    
    
"""
파이썬 웹툰데이타 클래스를 만들까? 만들어서 instance 로 id, title.. 저장하는게 더 빠르거나 깔끔하려나? 
getId 같은 함수만들어서 해도되고.. 지금은 리스트의 순서에 의존해서 구분하고 있으니까 클래스만드는게 깔끔할듯하다
"""

class webtoon_data:
    def __init__(self):
        pass