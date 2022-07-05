import json
import time
import traceback
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


################################# function setting ###############################################
def url_track_test(base_url, url_genre_list, count):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab
    genre_tag = url_genre_list[count]
    url = base_url + genre_tag
    driver.get(url)
    driver.implicitly_wait(300)
    
def get_data(webtoon_elements, genre):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)):
        # if webtoon_elements[i].find_element(By.XPATH, ".//img[@class='finish"):
        #     print("hello")
            
        # finish_status = webtoon_elements[i].find_element(By.XPATH, "").get_attribute()
        # 존재여부 어떻게 체크할지 : 시간?
        
        # link = webtoon_elements[i].find_element(By.XPATH, "").get_attribute() 
        # 필요없을듯? id로 ㄲ
    
        str_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("onclick")
        id = str_temp.split('\'')[3]
        rank = str_temp.split('\'')[5]
        title = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("title")
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "following::img").get_attribute("src")
        writer = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd/a").get_attribute("text")
        update_date = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[2]").text
        score = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[3]/div/strong").text
    
        webtoon_data_dict[id] = []
        webtoon_data_dict[id].append(genre)
        webtoon_data_dict[id].append(id)
        webtoon_data_dict[id].append(title)
        webtoon_data_dict[id].append(rank)
        webtoon_data_dict[id].append(thumbnail) 
        webtoon_data_dict[id].append(writer)
        webtoon_data_dict[id].append(update_date)
        webtoon_data_dict[id].append(score) 
    
    return webtoon_data_dict

"""
* 몇화 넣을까

design1 >> {genre1 : {id1 : [id, thumbnail, link(href), title, writer, finish_status, update_date, score]
            genre2 : {id2 : [...] ...}}
nested dict time : 
            
design2 >> {id1 : [*genre*, id, thumbnail, link, title, writer, finish_status, update_date, score],
            id2 : [..] .. }
one dict time:


div >   a(thumbnail)    > img(class="finish", default="연재")    > S
        dl()            > dt()                                  > a(href필요없겠다, title)
                        > dd(class="desc")                      > a(onclick=[2: id, 3: rank], text=writer)
                        > dd(class="date2")                     > update_date
                        > dd > div > strong.text = score
"""

################################# initial setting ###############################################
start = time.time()
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver") #mac
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Windows/chromedriver.exe") #win
################################################################################################

file = open("naver_genre.json","w")
url_genre_list = ["daily", "sensibility", "historical", "sports"] # 사이트별 설정 //
# ["daily", "comic", "fantasy", "action", "drama", "pure", "sensibility", "thrill", "historical", "sports"]
count = 0
webtoon_data_dict={}

for genre in url_genre_list:
    base_url = "https://comic.naver.com/webtoon/genre?genre="
    url_track_test(base_url, url_genre_list, count)
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, ".thumb") # webtoon element selection. 
    webtoon_elements.pop(0) # naver 장르별 첫 thumb 무시하기!
    webtoon_data_dict.update(get_data(webtoon_elements, genre))
    count += 1
    
print("######################################################################")   
print(webtoon_data_dict)
print("time :", time.time() - start)    

driver.close()
driver.quit()
json.dump(webtoon_data_dict, file, separators=(',', ':'))
file.close()    