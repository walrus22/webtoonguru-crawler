from collector_setting import *
import json
import time
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    count=0
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        driver.get(url)  
        # 다음 페이지 있으면 탐색 flag
        driver.implicitly_wait(2)
        ele = driver.find_elements(By.CLASS_NAME, "next")
        if len(ele) == 0:
            print("hi")
        ###################
        # 7.7 할일 
        # 1. 다음페이지 움직이면서 찾기
        # 2. 카카오 동적 탐색 (스크롤 몇번하고 하는지 아니면뭐 다른방법찾든지)
        # 3. 
        
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        genre_tag = genre_name[count]
        count+=1
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
        
        if 
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    rank_count = 1
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        id_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        id = id_temp[id_temp.index("worksseq=") + 9:]
        rank = rank_count
        rank += 1
        title = webtoon_elements[i].find_element(By.XPATH, "./a[@class='link']/div[@class='info']/strong").text
        thumbnail = webtoon_elements[i].find_element(By.XPATH, "./a[@class='link']/div[@class='thumb']/img").get_attribute("src")
        
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        driver.get(id_temp)
        
        ############# artist ###########
        author = driver.find_elements(By.CLASS_NAME, "authorInfoBtn")                
        artist = ""
        for i in author:
            artist += i.text
            if author.index(i) != len(author)-1:
                artist += ", "
        
        ############## day seperating. make func ######
        date_temp = driver.find_element(By.XPATH, "//p[@class='toon_author']/span[2]").text
        daylist = ["월", "화", "수", "목", "금", "토", "일"]
        if date_temp.find("완료") != -1:
            date = None
            finish_status = "완결"
        else:
            finish_status = "연재"
            for d in daylist:
                if date_temp.find(d) != -1:
                    date += d
                    if d != "일":
                        date += ", "
        ##############################################
        
        # etc_status = webtoon_elements[i].find_element(By.XPATH, ".") 
        
        webtoon_data_dict[id] = [] 
        webtoon_data_dict[id].append(genre_tag)
        webtoon_data_dict[id].append(id)
        webtoon_data_dict[id].append(rank)
        webtoon_data_dict[id].append(title)
        webtoon_data_dict[id].append(thumbnail)
        webtoon_data_dict[id].append(date)
        # webtoon_data_dict[id].append(etc_status)
        webtoon_data_dict[id].append(finish_status)
        webtoon_data_dict[id].append(artist)
        print(webtoon_data_dict)
        
    return webtoon_data_dict

################################################################################

start = time.time()
file = open("{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["123", "118", "3", "5", "1", "6", "8", "16", "109", "113"] # 로맨스, bl/gl, 개그, 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
genre_name = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
base_url = "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq={}"
css_tag = ".tm7"

json.dump(collect_webtoon_data(base_url, genre_list, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    