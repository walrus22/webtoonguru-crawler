import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

################################# function setting ###############################################
def collect_webtoon_data(base_url, genre_list, css_tag):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab
    webtoon_data_dict={}
    for genre_tag in genre_list:
        url = base_url + genre_tag
        driver.get(url)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_elements.pop(0) # naver 장르별 첫 thumb 무시하기!    
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)):
        # 화수?
        etc_status = ""
        finish_status = "연재"
        item_address = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("onclick")
        id = item_address.split('\'')[3]
        rank = item_address.split('\'')[5]
        title = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("title")
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "descendant::img").get_attribute("src")
        if len(webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")) != 1:
            if webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")[1].get_attribute("class") == "ico_cut":
                etc_status = "컷툰"
            else:
                etc_status = "신작"
        if len(webtoon_elements[i].find_elements(By.XPATH, "descendant::img")) != 1:
            finish_status = "완결"
        artist = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd/a").get_attribute("text")
        update_date = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[2]").text
        score = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[3]/div/strong").text
        webtoon_data_dict[id] = []
        webtoon_data_dict[id].append(genre_tag)
        webtoon_data_dict[id].append(id)
        webtoon_data_dict[id].append(item_address)
        webtoon_data_dict[id].append(rank)
        webtoon_data_dict[id].append(title)
        webtoon_data_dict[id].append(thumbnail)
        webtoon_data_dict[id].append(etc_status)
        webtoon_data_dict[id].append(finish_status)
        webtoon_data_dict[id].append(artist)
        webtoon_data_dict[id].append(update_date)
        webtoon_data_dict[id].append(score) 
    return webtoon_data_dict

################################# initial setting ###############################################
start = time.time()
chrome_options = Options()
# chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver") #mac
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Windows/chromedriver.exe") #win
driver.implicitly_wait(30)
################################################################################################

file = open("naver_genre.json","w")
genre_list = ["daily", "comic", "fantasy", "action", "drama", "pure", "sensibility", "thrill", "historical", "sports"] # 사이트별 설정 
# genre_list = ["sensibility","historical", "sports"] # 사이트별 설정 test
base_url = "https://comic.naver.com/webtoon/genre?genre="

json.dump(collect_webtoon_data(base_url, genre_list, css_tag = ".thumb"), file, separators=(',', ':'))
print("time :", time.time() - start)    
driver.close()
driver.quit()
file.close()    


# TODO: try-catch, 화수, 서비스 플랫폼, 요일, 휴재, 업로드여부, 성인