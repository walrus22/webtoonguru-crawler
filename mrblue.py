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
    item_rank = 0
    address_list = []
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        address_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        item_id = address_temp[12:]
        item_address = "https://www.mrblue.com" + address_temp
        # 아니씨발이게 맥이랑 가져오는 형식이 다른가?
        # 윈도우에선 address_temp가 전체 주소를 가져오고, mac에선 안가져왔는데 ㅡㅡ 씨발
        
        address_list.append(item_address)
        item_rank += 1
        webtoon_data_dict[item_id] = []
        webtoon_data_dict[item_id].append(genre_tag)
        webtoon_data_dict[item_id].append(item_id)
        webtoon_data_dict[item_id].append(item_address)
        webtoon_data_dict[item_id].append(item_rank)
        
    for child_url in address_list:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, child_url) 
        
        item_title = driver.find_element(By.CLASS_NAME, 'title').text
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[1]").text, "완결")
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='img-box']/p/img").get_attribute("src")
        # item_etc_status = 
    
        # 그림/글 : 1명 // 그림 ~명 글 ~명 2가지 케이스 있다
        item_artist = ""
        first = True
        for author in driver.find_elements(By.CLASS_NAME, 'authorname'):
            if first == True:
                first = False
            else:
                item_artist += ","
        
        webtoon_data_dict[item_id].append(item_title)
        webtoon_data_dict[item_id].append(item_date)
        webtoon_data_dict[item_id].append(item_thumbnail)
        # webtoon_data_dict[item_id].append(item_etc_status)
        webtoon_data_dict[item_id].append(item_finish_status)
        webtoon_data_dict[item_id].append(item_artist)
        
    return webtoon_data_dict

################################################################################
start = time.time()
file = open("json//{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["romance", "bl", "drama", "gl", "action", "fantasy", "thriller"] # 성인있음 erotic
base_url = "https://www.mrblue.com/webtoon/genre/{}?sortby=rank"
css_tag = ".img"

# login
user_id = "tuntunjun@naver.com"
user_password = "Test123!@#"
get_url_untill_done(driver, "https://www.mrblue.com/webtoon/wt_000052546") 
driver.find_element(By.ID, "pu-page-id").send_keys(user_id)
driver.find_element(By.ID, "pu-page-pw").send_keys(user_password)
time.sleep(2)
driver.find_element(By.ID, "pu-page-pw").send_keys(Keys.ENTER)

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    