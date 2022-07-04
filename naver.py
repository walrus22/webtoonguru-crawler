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

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Windows/chromedriver.exe")

url = "https://comic.naver.com/webtoon/weekday"


src_dict = {}
day_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


            
driver.get(url)
time.sleep(2)
test_list = {}
test = driver.find_elements_by_css_selector(".thumb")




# for i in range(10):
#     test_list[] = []
#     test[i].find_element_by_xpath("following-sibling::a").get_attribute("href")
#     print(test[i].find_element_by_xpath("following-sibling::a").get_attribute("title"))
#     print("######################################################################")
    
    


    

# find_element return값이 뭐임? 
# 이게 부모 추적이 가능한가?

# <a href="/webtoon/list?titleId=758037&amp;weekday=mon" onclick="nclk_v2(event,'thm*m.tit','','1')" class="title" title="참교육">참교육</a>

"""
TODO: ㅎㅎ
 1. 요일별 class = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
 2. li or class=thumb 순서대로 탐색, 순위 할당 
 3. href로 titleId 태깅, ID 리스트 저장  (*https://comic.naver.com/webtoon/list?titleId=758037 (titleId로 접근가능)
 4. class="title"저장하든지 아니면 링크탔을때 저장
 5. 날짜 끝나면? or 그냥 일욜까지 추적 다하고?
 6. 링크타고 들어감
 7. 일단 최신화 정보 & 별점 & 하트수 & 시놉시스 등 딕셔너리 저장
 8. class="cnt_page"로 다음페이지 이동하면서 탐색끝까지 하던지 그건 나중에 ㄱㄱ
"""




# import requests
# from lxml import etree
# import time
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
 
# # Launch Chrome browser in headless mode
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# browser = webdriver.Chrome(options=options)
 
# # Load web page
# browser.get("https://www.yahoo.com")
# # Network transport takes time. Wait until the page is fully loaded
# def is_ready(browser):
#     return browser.execute_script(r"""
#         return document.readyState === 'complete'
#     """)
# WebDriverWait(browser, 30).until(is_ready)
 
# # Scroll to bottom of the page to trigger JavaScript action
# browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(1)
# WebDriverWait(browser, 30).until(is_ready)
 
# # Search for news headlines and print
# elements = browser.find_elements(By.XPATH, "//h3/a[u[@class='StretchedBox']]")
# for elem in elements:
#     print(elem.text)
 
# # Close the browser once finish
# browser.close()