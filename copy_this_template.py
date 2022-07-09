from collector_setting import *
import json
from pathlib import Path

### After kakao new, 그냥 url만 주고 하나씩 접속해서 따는게 낫겠다. 굳이 앞에서 이것저것 따올필요가 없었네;;
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    webtoon_elements_url = []
    
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        get_url_untill_done(driver, url)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        for elements in webtoon_elements:
            webtoon_elements_url += elements.get_attribute("href")
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_id_list = []
    item_address_list = []
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        
        item_id = driver.find_element(By.XPATH, "")
        item_id = item_address[:]
        item_id_list.append(item_id)
        
        item_rank += 1
        # item_rank = webtoon_elements[i].find_element(By.XPATH, "") # choose one
        item_thumbnail = driver.find_element(By.XPATH, "")
        item_title = driver.find_element(By.XPATH, "")
        item_date, item_finish_status = find_date(item_date_temp=driver.find_element(By.XPATH, ""), end_comment= , day_keyword=, daylist_more=)
        item_synopsis = driver.find_element(By.XPATH, "")
        item_artist = driver.find_element(By.XPATH, "")
        item_etc_status = driver.find_element(By.XPATH, "")
        # item_date = 
        # item_finish_status = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [genre_tag, item_id, item_address, item_rank, item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist]

###########################################################################

start = time.time()
file = open(os.getcwd() + "/sab-git-test/json/{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["",] # 사이트별 설정 
base_url = ""
css_tag = ""


login_for_adult

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    

################################# old setting ############################
# def collect_webtoon_data(base_url, genre_list, css_tag):
#     # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
#     webtoon_data_dict={}
#     for genre_tag in genre_list:
#         url = base_url.format(genre_tag)
#         get_url_untill_done(driver, url)
#         webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
#         webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
#     return webtoon_data_dict
    
# def get_element_data(webtoon_elements, genre_tag):
#     webtoon_data_dict = {}
#     item_id_list = []
#     item_address_list = []
#     item_rank = 0
    
#     for i in range(len(webtoon_elements)): # len(webtoon_elements)
#         item_address = webtoon_elements[i].find_element(By.XPATH, "")
#         item_address_list.append(item_address)    
#         item_id = webtoon_elements[i].find_element(By.XPATH, "")
#         # itme_id = item_address[:]
#         item_id_list.append(item_id)
        
#         item_rank += 1
#         # item_rank = webtoon_elements[i].find_element(By.XPATH, "") # choose one

#         webtoon_data_dict[item_id] = []
#         webtoon_data_dict[item_id].append(genre_tag)
#         webtoon_data_dict[item_id].append(item_id)
#         webtoon_data_dict[item_id].append(item_address)
#         webtoon_data_dict[item_id].append(item_rank)

#     for j in range(len(webtoon_elements)):
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
#         get_url_untill_done(driver, item_address_list[j])
        
#         item_thumbnail = driver.find_element(By.XPATH, "")
#         item_title = driver.find_element(By.XPATH, "")
#         item_date, item_finish_status = find_date(item_date_temp=driver.find_element(By.XPATH, ""), end_comment= , day_keyword=, daylist_more=)
#         item_synopsis = driver.find_element(By.XPATH, "")
#         item_artist = driver.find_element(By.XPATH, "")
#         item_etc_status = driver.find_element(By.XPATH, "")
        
#         # item_date = 
#         # item_finish_status = driver.find_element(By.XPATH, "")
        
#         webtoon_data_dict[item_id_list[j]].append(item_thumbnail)
#         webtoon_data_dict[item_id_list[j]].append(item_title)
#         webtoon_data_dict[item_id_list[j]].append(item_date)
#         webtoon_data_dict[item_id_list[j]].append(item_finish_status)
#         webtoon_data_dict[item_id_list[j]].append(item_synopsis)
#         webtoon_data_dict[item_id_list[j]].append(item_artist)
#         webtoon_data_dict[item_id_list[j]].append(item_etc_status)
        
#     return webtoon_data_dict
################################################################################