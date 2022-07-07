from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, css_tag):
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
    
    # 하나씩 클릭하면서 접근
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        item_address = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        item_address_list.append(item_address)
        item_id = item_address[item_address.index("worksseq=") + 9:]
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
    
    for j in webtoon_data_dict.values():
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, j[2]) # item_address_list 쓰셈.. iterator 돌려서 append해
        # for 
        #
        #
        #
        ############# item_artist ###########
        artist_list = driver.find_elements(By.CLASS_NAME, "authorInfoBtn")                
        item_artist = ""
        for k in artist_list:
            item_artist += k.text
            if artist_list.index(k) != len(artist_list)-1:
                item_artist += ", "
                
        ############## day seperating. make func ######
        item_date_temp = driver.find_element(By.XPATH, "//p[@class='toon_author']/span[2]").text
        daylist = ["월", "화", "수", "목", "금", "토", "일"]
        item_date=""
        if item_date_temp.find("완료") != -1:
            item_date = "완결"
            item_finish_status = "완결"
        else:
            item_finish_status = "연재"
            for d in daylist:
                if item_date_temp.find(d) != -1:
                    if d == "일" and item_date_temp.find("일 요일") == -1: # 만약 일 위치가 마지막이면 무시
                        break
                    item_date += d                            
        ##############################################
        webtoon_data_dict[j[1]].append(item_date)
        # webtoon_data_dict[item_id].append(etc_status)
        # etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
        # 하트수?
        webtoon_data_dict[j[1]].append(item_finish_status)
        webtoon_data_dict[j[1]].append(item_artist)
    return webtoon_data_dict

################################################################################

start = time.time()
file = open("{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

# genre_list = ["1", "6", "8", "16", "109", "113"] # 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
genre_list = ["123", "118", "3", "5", "1", "6", "8", "16", "109", "113"] # 로맨스, bl/gl, 개그, 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
genre_name = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
base_url = "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq={}"
css_tag = ".tm7"

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    

#