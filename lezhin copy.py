import json
import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


################################# function setting ###############################################
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab
    webtoon_data_dict={}
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        # time.sleep(2)
        driver.get(url)  
        # time.sleep(15)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)): #len(webtoon_elements)
        # etc_status = ""
        # finish_status = "연재"
        # str_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("onclick")
        # id = str_temp.split('\'')[3]
        # rank = str_temp.split('\'')[5]
        # title = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("title")
        # thumbnail = webtoon_elements[i].find_element(By.XPATH, "descendant::img").get_attribute("src")
        # if len(webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")) != 1:
        #     if webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")[1].get_attribute("class") == "ico_cut":
        #         etc_status = "컷툰"
        #     else:
        #         etc_status = "신작"
        # if len(webtoon_elements[i].find_elements(By.XPATH, "descendant::img")) != 1:
        #     finish_status = "완결"
        # artist = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd/a").get_attribute("text")
        # update_date = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[2]").text
        # score = webtoon_elements[i].find_element(By.XPATH, "following-sibling::dl/dd[3]/div/strong").text
        
        # print(webtoon_elements[i].find_element(By.XPATH, "//p[@class='lzComic__title']").get_attribute("href"))
        id = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute('href')[32:]
        rank = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__count']/strong[@class='lzComic__rank']").text
        title = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__info']/p[@class='lzComic__title']").text
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__thumb']/picture[@class='lzComic__img']/source").get_attribute("srcset")
        # etc_status = webtoon_elements[i].find_element(By.XPATH, ".") #new
        # finish_status = webtoon_elements[i].find_element(By.XPATH, ".")
        artist = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__info']/p[@class='lzComic__meta']/span[@class='lzComic__artist']").text
        
        webtoon_data_dict[id] = []
        webtoon_data_dict[id].append(genre_tag)
        webtoon_data_dict[id].append(id)
        webtoon_data_dict[id].append(rank)
        webtoon_data_dict[id].append(title)
        webtoon_data_dict[id].append(thumbnail)
        # webtoon_data_dict[id].append(etc_status)
        # webtoon_data_dict[id].append(finish_status)
        webtoon_data_dict[id].append(artist)
    return webtoon_data_dict

################################# initial setting ###############################################
start = time.time()

os.environ['WDM_LOG_LEVEL'] = '0'

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument("--log-level=OFF")
# options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(300)
file = open("{}.json".format(Path(__file__).stem), "w")
################################################################################################

genre_list = ["romance", "bl", "drama", "fantasy", "gag", "action", "school", "mystery", "day", "gl"] # 사이트별 설정 
base_url = "https://www.lezhin.com/ko/ranking/detail?genre=romance&type=realtime"
css_tag = ".lzComic__item"

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()

file.close()    


# TODO: try-catch, 화수, 서비스 플랫폼, 요일, 휴재, 업로드여부, 성인