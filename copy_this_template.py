from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        get_url_untill_done(driver, url)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        
        item_item_id = webtoon_elements[i].find_element(By.XPATH, "")
        item_address = webtoon_elements[i].find_element(By.XPATH, "")
        item_rank = webtoon_elements[i].find_element(By.XPATH, "")
        item_title = webtoon_elements[i].find_element(By.XPATH, "")
        item_date = webtoon_elements[i].find_element(By.XPATH, "")
        item_thumbnail = webtoon_elements[i].find_element(By.XPATH, "")
        item_etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
        item_finish_status = webtoon_elements[i].find_element(By.XPATH, ".")
        item_artist = webtoon_elements[i].find_element(By.XPATH, "")
        
        # webtoon_data_dict[item_id] = []
        # webtoon_data_dict[item_id].append(genre_tag)
        # webtoon_data_dict[item_id].append(item_item_id)
        # webtoon_data_dict[item_id].append(item_item_address)
        # webtoon_data_dict[item_id].append(item_rank)
        # webtoon_data_dict[item_id].append(item_title)
        # webtoon_data_dict[item_id].append(item_date)
        # webtoon_data_dict[item_id].append(item_thumbnail)
        # webtoon_data_dict[item_id].append(item_etc_status)
        # webtoon_data_dict[item_id].append(item_finish_status)
        # webtoon_data_dict[item_id].append(item_artist)
        
    return webtoon_data_dict

################################################################################
start = time.time()
file = open("json//{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["",] # 사이트별 설정 
base_url = ""
css_tag = ""

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    