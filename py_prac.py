import os
import time
import random
from PIL import Image
from urllib.request import urlopen
from selenium import webdriver


from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(url, genre_tag, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    driver = driver_set()
    get_url_untill_done(driver, url)
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
    webtoon_data_dict.update(get_element_data(driver, webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(driver, webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    item_address_list = []
    item_id_list = []
    
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        item_address = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        item_id = item_address[31:]
        item_id_list.append(item_id)
        item_address_list.append(item_address)    
        item_rank += 1
        
        # address_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        # item_id = address_temp[12:]
        # item_address = "https://www.mrblue.com" + address_temp
        # 아니씨발이게 맥이랑 가져오는 형식이 다른가?
        # 윈도우에선 address_temp가 전체 주소를 가져오고, mac에선 안가져왔는데 ㅡㅡ 씨발 
        # 7.8 뭐야 맥북에서도 전체주소 가져오네 ㅡㅡ
        # 근본없는 사이트다운 주소 태그다
        
        webtoon_data_dict[item_id] = []
        webtoon_data_dict[item_id].append(genre_tag)
        webtoon_data_dict[item_id].append(item_id)
        webtoon_data_dict[item_id].append(item_address)
        webtoon_data_dict[item_id].append(item_rank)
        
    for j in range(len(webtoon_elements)):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, item_address_list[j])
        
        item_title = driver.find_element(By.CLASS_NAME, 'title').text
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[1]").text, "완결", False)
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='img-box']/p/img").get_attribute("src")
        # item_etc_status = 
        # synopsis
    
        # 그림/글 : 1명 // 그림 ~명 글 ~명 2가지 케이스 있다
        item_artist = ""
        first = True
        for author in driver.find_elements(By.CLASS_NAME, 'authorname'):
            if first == True:
                first = False
            else:
                item_artist += ","
        
        webtoon_data_dict[item_id_list[j]].append(item_title)
        webtoon_data_dict[item_id_list[j]].append(item_date)
        webtoon_data_dict[item_id_list[j]].append(item_thumbnail)
        # webtoon_data_dict[item_id_list[j]].append(item_etc_status)
        webtoon_data_dict[item_id_list[j]].append(item_finish_status)
        webtoon_data_dict[item_id_list[j]].append(item_artist)
        
    return webtoon_data_dict

################################################################################


import pickle

# store
driver = driver_set()
get_url_untill_done(driver, "https://webtoon.kakao.com/")
# time.sleep(50)
# cookie_list = driver.get_cookies()
# pickle.dump(cookie_list, open("kakao_cookies.pkl","wb"))  
 
# load
cookie_list = pickle.load(open("kakao_cookies.pkl", "rb"))
for cookie in cookie_list:
    driver.add_cookie(cookie)
get_url_untill_done(driver, "https://webtoon.kakao.com/")

time.sleep(30)

# # cmd : cd C:\Program Files\Google\Chrome\Application 
# # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTemp"
