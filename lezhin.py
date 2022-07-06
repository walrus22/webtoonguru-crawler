from collector_setting import *
import json
import time
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        driver.get(url)  
        # time.sleep(15)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)): #len(webtoon_elements)
        id = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute('href')[32:]
        rank = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__count']/strong[@class='lzComic__rank']").text
        title = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__info']/p[@class='lzComic__title']").text
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "./a[@class='lzComic__link']/div[@class='lzComic__thumb']/picture[@class='lzComic__img']/source").get_attribute("srcset")
        # etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
        # 연재태그 수정
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

################################################################################

start = time.time()
file = open("{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["romance", "bl", "drama", "fantasy", "gag", "action", "school", "mystery", "day", "gl"] # 사이트별 설정 
base_url = "https://www.lezhin.com/ko/ranking/detail?genre={}&type=realtime"
css_tag = ".lzComic__item"

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    