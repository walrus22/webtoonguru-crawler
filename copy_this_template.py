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
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        
        id = webtoon_elements[i].find_element(By.XPATH, "")
        rank = webtoon_elements[i].find_element(By.XPATH, "")
        title = webtoon_elements[i].find_element(By.XPATH, "")
        date = webtoon_elements[i].find_element(By.XPATH, "")
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "")
        etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
        finish_status = webtoon_elements[i].find_element(By.XPATH, ".")
        artist = webtoon_elements[i].find_element(By.XPATH, "")
        
        # webtoon_data_dict[id] = []
        # webtoon_data_dict[id].append(genre_tag)
        # webtoon_data_dict[id].append(id)
        # webtoon_data_dict[id].append(rank)
        # webtoon_data_dict[id].append(title)
        # webtoon_data_dict[id].append(date)
        # webtoon_data_dict[id].append(thumbnail)
        # webtoon_data_dict[id].append(etc_status)
        # webtoon_data_dict[id].append(finish_status)
        # webtoon_data_dict[id].append(artist)
        
    return webtoon_data_dict

################################################################################

start = time.time()
file = open("{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["",] # 사이트별 설정 
base_url = ""
css_tag = ""

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    