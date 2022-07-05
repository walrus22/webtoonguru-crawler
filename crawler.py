from ast import Try
from re import A
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
import sys
import json

file = open("naver_test.json","w")

# try:

# except Exception:
#       print(Exception)
#     # print(traceback.format_exc())

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver") #mac
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Windows/chromedriver.exe") #win

# day_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

start = time.time()
url = "https://comic.naver.com/webtoon/weekday"
driver.get(url)
driver.implicitly_wait(100)
test = driver.find_elements(By.CSS_SELECTOR, ".thumb") ## 집 selenium update
test_list = {}

for i in range(len(test)): # len(test)
    str_temp = test[i].find_element(By.XPATH, "following-sibling::a").get_attribute("href")
    id_temp = str_temp[str_temp.index("titleId=") + 8 : str_temp.index("&")] 
    day = str_temp[str_temp.index("weekday=") + 8 : ]
    
    if (test_list.get(id_temp) != None):
        test_list[id_temp][3].append(day) # additional day, 3 = index of day
        continue
    else:
        test_list[id_temp] = []
                   
    title_temp = test[i].find_element(By.XPATH, "following-sibling::a").get_attribute("title")
    test_list[id_temp].append(id_temp)
    test_list[id_temp].append(str_temp) # link
    test_list[id_temp].append(title_temp) # title
    test_list[id_temp].append([day]) # day
        
print("######################################################################")   
# print(test_list)
print("time :", time.time() - start) 
print("######################################################################")   

for el in test_list.values():
    url_writer = el[1]  
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab
    driver.get(url_writer)
    driver.implicitly_wait(500)

    synop = driver.find_element(By.XPATH, "//div[@class='detail']/child::p").text
    writer = driver.find_element(By.CSS_SELECTOR, ".wrt_nm").text
    genre = driver.find_element(By.CSS_SELECTOR, ".genre").text
    age_restrict = driver.find_element(By.CSS_SELECTOR, ".age").text
    like_count = driver.find_element(By.CSS_SELECTOR, ".u_cnt").text 
    
    test_list[el[0]].append(synop) # synop
    test_list[el[0]].append(writer) # writer
    test_list[el[0]].append(genre) # genre
    test_list[el[0]].append(age_restrict) # age_restrict
    test_list[el[0]].append(like_count) # like_count
    
    
driver.close()
driver.quit()
print("######################################################################")   
print(test_list)
print("######################################################################")
print("time :", time.time() - start)    

json.dump(test_list, file, separators=(',', ':'))
file.close()
    
# class Crawler:
#     def __init__(self, base_url): # target base page 
#         self.base_url = base_url
#         self.id_list = []


"""
1. 요일별 class = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
2. li or class=thumb 순서대로 탐색, 순위 할당 
3. href로 titleId 태깅, ID 리스트 저장  (*https://comic.naver.com/webtoon/list?titleId=758037 (titleId로 접근가능)
4. class="title"저장하든지 아니면 링크탔을때 저장
5. 날짜 끝나면? or 그냥 일욜까지 추적 다하고?
6. 링크타고 들어감
7. 일단 최신화 정보 & 별점 & 하트수 & 시놉시스 등 딕셔너리 저장

TODO:
8. class="cnt_page"로 다음페이지 이동하면서 탐색끝까지 하던지 그건 나중에 ㄱㄱ
9. 최적화
"""
