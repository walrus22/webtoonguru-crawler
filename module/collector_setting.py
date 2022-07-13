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

import mysql.connector
import datetime

def driver_set():
    options = Options()
    # options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080") # for chrome
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
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
    driver.implicitly_wait(300)
    return driver

def get_url_untill_done(driver_var, url, random_min=1, random_max=3):
    count = 1
    for i in range(1, 10): # limit trying
        try:
            # 시간 바꾸지마라.. 밴당해 디도스로
            driver_var.implicitly_wait(30)
            time.sleep(random.uniform(random_min,random_max)) # prevent to restrict
            driver_var.get(url)
            time.sleep(random.uniform(random_min,random_max))
            print(url + " << " + str(count) + " time try, success!") #, end=""
            break
        except Exception as e:
            driver_var.implicitly_wait(30)
            # print(str(e) + " << " + url + " << " + str(count) + " time try, failed!")
            print(url + " << " + str(count) + " time try, failed.")
            time.sleep(15) # without headless
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
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, id_tag).send_keys(user_id)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(user_pw)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(Keys.ENTER)
    time.sleep(random.uniform(5,7))

def is_adult(item_adult_string, key_word):
    if item_adult_string.find(key_word) != -1: # adult
        return True
    else:
        return False


class mysql_db:
    def __init__(self, db_name):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Zmfhffldxptmxm123!@#",
        database=db_name
        )
        self.cursor = self.db.cursor()
        
    def create_table(self, table_name):
        self.cursor.execute("Create TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, item_id VARCHAR(255), item_genre VARCHAR(255), item_address VARCHAR(255), item_rank int, item_thumbnail VARCHAR(255), item_title VARCHAR(255), item_date VARCHAR(255), item_finish_status VARCHAR(255), item_synopsis VARCHAR(255), item_artist VARCHAR(255), item_adult boolean)".format(table_name))
        
    def insert_to_mysql(self, list_element, table_name):
        str_temp=""
        first = True
        for i in list_element:
            if first == True:
                str_temp += '\'{}\''.format(i)
                first = False
            elif type(i) != str:
                str_temp += ',{}'.format(i)
            else: 
                str_temp += ',\'{}\''.format(i)

        self.cursor.execute("INSERT INTO {table} (item_id, item_genre, item_address, item_rank, item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult) VALUES ({value_str})".format(table=table_name, value_str=str_temp))
        
        print(self.cursor.rowcount, "record inserted")

"""
파이썬 웹툰데이타 클래스를 만들까? 만들어서 instance 로 id, title.. 저장하는게 더 빠르거나 깔끔하려나? 
getId 같은 함수만들어서 해도되고.. 지금은 리스트의 순서에 의존해서 구분하고 있으니까 클래스만드는게 깔끔할듯하다
"""

class webtoon_data:
    def __init__(self):
        pass