from ast import Try
from re import A
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import traceback
import sys
# class Crawler:
#     def __init__(self, url):
#         self.url = url

# try:

# except Exception:
#       print(Exception)
#     # print(traceback.format_exc())
start = time.time()

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Windows/chromedriver.exe")

url = "https://comic.naver.com/webtoon/weekday"

day_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
driver.get(url)
time.sleep(2)
test_list = {}
test = driver.find_elements_by_css_selector(".thumb")


for i in range(len(test)):
    str_temp = test[i].find_element_by_xpath("following-sibling::a").get_attribute("href")
    id_temp = str_temp[str_temp.index("titleId=") + 8 : str_temp.index("&")] 
    day_temp = str_temp[str_temp.index("weekday=") + 8 : ]
    title_temp = test[i].find_element_by_xpath("following-sibling::a").get_attribute("title")
    test_list[id_temp] = []
    test_list[id_temp].append(title_temp)
    test_list[id_temp].append(day_temp)
    
print("######################################################################")   
print(test_list)
print("######################################################################")   
print("time :", time.time() - start)   
    

"""
 1. 요일별 class = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
 2. li or class=thumb 순서대로 탐색, 순위 할당 
 3. href로 titleId 태깅, ID 리스트 저장  (*https://comic.naver.com/webtoon/list?titleId=758037 (titleId로 접근가능)
 4. class="title"저장하든지 아니면 링크탔을때 저장
 5. 날짜 끝나면? or 그냥 일욜까지 추적 다하고?
 
 TODO:
 6. 링크타고 들어감
 7. 일단 최신화 정보 & 별점 & 하트수 & 시놉시스 등 딕셔너리 저장
 8. class="cnt_page"로 다음페이지 이동하면서 탐색끝까지 하던지 그건 나중에 ㄱㄱ
"""
