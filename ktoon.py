from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, genre_name, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    count=0
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, url)
               
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        genre_tag = genre_name[count]
        rank_basis = 0
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag, rank_basis))
        count+=1
        # 다음 페이지 있으면 탐색 flag
        while True:
            get_url_untill_done(driver, url)
            driver.implicitly_wait(2)
            next_page_element = driver.find_elements(By.CLASS_NAME, "next")
            if len(next_page_element) == 0:
                break
            else: 
                # driver.implicitly_wait(300)
                rank_basis+=len(webtoon_elements)
                url = next_page_element[0].find_element(By.XPATH, "./a").get_attribute("href")
                get_url_untill_done(driver, url)
                driver.implicitly_wait(2)
                if len(driver.find_elements(By.CLASS_NAME, "tm7")) == 0: # there is next page but no elements
                    break
                webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection.         
                webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag, rank_basis))
        ###################
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag, rank_basis):
    webtoon_data_dict = {}
    item_rank = rank_basis
    item_address_list=[]
    item_id_list = []

    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        item_address = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        item_address_list.append(item_address)
        item_id = item_address[item_address.index("worksseq=") + 9:]
        item_id_list.append(item_id)
        
        item_rank += 1
        item_title = webtoon_elements[i].find_element(By.XPATH, "./a[@class='link']/div[@class='info']/strong").text
        item_thumbnail = webtoon_elements[i].find_element(By.XPATH, "./a[@class='link']/div[@class='thumb']/img").get_attribute("src")
        
        webtoon_data_dict[item_id] = [] 
        webtoon_data_dict[item_id].append(genre_tag)
        webtoon_data_dict[item_id].append(item_id)
        webtoon_data_dict[item_id].append(item_address)
        webtoon_data_dict[item_id].append(item_rank)
        webtoon_data_dict[item_id].append(item_title)
        webtoon_data_dict[item_id].append(item_thumbnail)
    
    # 하나씩 클릭하면서 접근ß
    for j in range(len(webtoon_elements)):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, item_address_list[j])
        
        ############# item_artist ###########
        artist_list = driver.find_elements(By.CLASS_NAME, "authorInfoBtn")                
        item_artist = ""
        for k in artist_list:
            item_artist += k.text
            if artist_list.index(k) != len(artist_list)-1:
                item_artist += ", "
                
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//p[@class='toon_author']/span[2]").text, "완료", True)
        item_synopsis = driver.find_element(By.CLASS_NAME, "toon_copy").text
        
        webtoon_data_dict[item_id_list[j]].append(item_date)
        webtoon_data_dict[item_id_list[j]].append(item_finish_status)
        webtoon_data_dict[item_id_list[j]].append(item_artist)
        webtoon_data_dict[item_id_list[j]].append(item_synopsis)
        # webtoon_data_dict[item_id].append(etc_status)
        # etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
    return webtoon_data_dict
################################################################################

start = time.time()
file = open(os.path.join(os.getcwd(), "json", "{}test.json".format(Path(__file__).stem)), "w")
driver = driver_set()

# genre_list = ["1", "6", "8", "16", "109", "113"] # 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
genre_list = ["123", "118", "3", "5", "1", "6", "8", "16", "109", "113"] # 로맨스, bl/gl, 개그, 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
genre_name = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
base_url = "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq={}"
css_tag = ".tm7"

json.dump(collect_webtoon_data(base_url, genre_list, genre_name, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    

#