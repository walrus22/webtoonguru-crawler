from mimetypes import init
import os
import time
import random
import json
from multiprocessing import Pool, Manager

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 이동해야 하는 경우 등 키입력시 사용

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# import mysql.connector
import datetime
from pymongo import MongoClient

def driver_set():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080") # for chrome
    options.add_argument("--disable-gpu")    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #### chrome #####
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # chrome_driver = "/usr/local/bin/chromedriver" # Mac Chrome Driver path
    # chrome_driver = "C:\\Python\\chromedriver.exe" # Windows Chrome Driver path
    # driver = webdriver.Chrome(chrome_driver, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # # cmd : cd C:\Program Files\Google\Chrome\Application 
    # # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTemp"
    # mac: sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
    # http://localhost:9222/ 접속되는지 확인
    # driver.set_window_position(2560, 0) # for imac dual monior
    # driver.set_window_position(3520, 0) # for imac dual monior
    driver.implicitly_wait(100)
    return driver

def get_url_untill_done(driver_var, url, random_min=2, random_max=3):
    count = 1
    for i in range(1, 10): # limit trying
        try:
            # 시간 바꾸지마라.. 밴당해 디도스로
            # driver_var.implicitly_wait(30)
            # time.sleep(random.uniform(random_min,random_max)) # prevent to restrict
            driver_var.get(url)
            time.sleep(random.uniform(random_min,random_max))
            print(url + " << " + str(count) + " time try, success!") #, end=""
            break
        except Exception as e:
            # driver_var.implicitly_wait(30)
            # print(str(e) + " << " + url + " << " + str(count) + " time try, failed!")
            print(url + " << " + str(count) + " time try, failed.")
            time.sleep(10) # without headless
            count+=1
            if i == 10:
                raise
            continue     

def catch_duplicate(webtoon_data_dict_temp, shared_dict):
    for key in list(webtoon_data_dict_temp): 
        if key in shared_dict.keys  ():
            shared_temp = shared_dict[key]
            shared_temp[1]+= (webtoon_data_dict_temp[key][1]) # genre
            shared_temp[3]+= (webtoon_data_dict_temp[key][3]) # rank
            shared_dict[key] = shared_temp
            webtoon_data_dict_temp.pop(key) 
    shared_dict.update(webtoon_data_dict_temp)

def collect_multiprocessing(pool_size, collect_webtoon_data, base_url, genre_list, cookie_list=[], genre_name=[]):
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    if len(genre_name) != 0:
        genre_list = genre_name
    
    manager = Manager()
    shared_dict = manager.dict()
    
    pool = Pool(pool_size) 
    for i in range(len(url_list)):  #len(url_list)
        pool.apply_async(collect_webtoon_data, args =(shared_dict, url_list[i], genre_list[i], cookie_list))        
        time.sleep(random.uniform(0.7,1.5))
    pool.close()
    pool.join() 
    
    shared_dict_copy = shared_dict.copy() 
    return shared_dict_copy

def find_date(date_temp : str, end_comment, day_keyword, daylist_more=[]): # , day_keyword=False "요일" 있으면 True
    date_temp = date_temp.replace(" ","") 
    daylist = ["월", "화", "수", "목", "금", "토", "일"]
    first_append = True
    date = ""
    
    if len(daylist_more) != 0:
        daylist = daylist_more + daylist
    if date_temp.find(end_comment) != -1: # end_comment = 완료?
        date = "완결"
        finish_status = "완결"
    else:
        finish_status = "연재"
        for d in daylist:
            if date_temp.find(d) != -1:
                if d == "일" and day_keyword == True and date_temp.find("일요일") == -1:
                    break                    
                if first_append == True:
                    date += d
                    first_append = False
                else:                    
                    date += "," + d
        if date == "":
            date = "비정기"
    return date, finish_status     

def insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult):
    # 8.6 separate genre
    if type(item_genre) == list:
        item_rank = [item_rank] * len(item_genre)
        webtoon_data_dict[item_id] = [item_id, item_genre, item_address, item_rank, item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    else :
        webtoon_data_dict[item_id] = [item_id, [item_genre], item_address, [item_rank], item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
def is_adult(adult_string, key_word):
    if adult_string.find(key_word) != -1: # adult
        return True
    else:
        return False       

def save_as_json(path_cwd, file_name, shared_dict_copy, start_time):
    with open(os.path.join(path_cwd, "module", "json", "{}.json".format(file_name)), "w") as file:
        json.dump(shared_dict_copy, file, separators=(',', ':'))
    print("{} >> ".format(file_name), time.time() - start_time)   

def login_for_adult(driver, user_id, user_pw, id_tag, pw_tag):
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, id_tag).send_keys(user_id)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(user_pw)
    time.sleep(random.uniform(2,3))
    driver.find_element(By.XPATH, pw_tag).send_keys(Keys.ENTER)
    time.sleep(random.uniform(3,5))



