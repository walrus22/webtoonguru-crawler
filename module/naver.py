from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_without_cookie(shared_dict, url, genre_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []
    
    # collect item url    
    driver = driver_set()
    get_url_untill_done(driver, url)
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, ".thumb") # webtoon element selection. 
    webtoon_elements.pop(0) # naver 장르별 첫 thumb 무시하기!    
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    # webtoon_elements_url = ["https://comic.naver.com/webtoon/list?titleId=758037"]    
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    driver.close()
    return shared_dict
        
    
def get_element_data(driver, webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: 
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        item_rank += 1
        item_id = item_address[item_address.rfind("=")+1:]
        
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='comicinfo']/div/a/img").get_attribute("src")
        item_title = driver.find_element(By.XPATH, "//div[@class='detail']/h2/span[1]").text
        item_artist = driver.find_element(By.XPATH, "//span[@class='wrt_nm']").text
        item_synopsis = driver.find_element(By.XPATH, "//div[@class='detail']/p").text
        item_adult = driver.find_element(By.XPATH, "//span[@class='age']").text
        if item_adult.find("18세") != -1: # adult
            item_adult = True
        else:
            item_adult = False
        
        # if len(webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")) != 1:
        # if webtoon_elements[i].find_elements(By.XPATH, "child::a/child::span")[1].get_attribute("class") == "ico_cut":
        #     etc_status = "컷툰"
        # else:
        #     etc_status = "신작"
    
        # temporarily store
        item_date = "완결"
        item_finish_status = "완결"
        
        webtoon_data_dict[item_id] = [item_id, genre_tag, item_address, item_rank, item_thumbnail, 
                                      item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_without_cookie(shared_dict, url_list, genre_list):
    pool = Pool(1) 
    for i in range(len(url_list)):   #len(url_list)
        pool.apply_async(collect_webtoon_data_without_cookie, args =(shared_dict, url_list[i], genre_list[i]))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w")
    print(os.path.join(os.getcwd(), "json", "{}.json".format(Path(__file__).stem)))
    # genre_list = ["historical", "sports"]
    genre_list = ["daily", "comic", "fantasy", "action", "drama", "pure", "sensibility", "thrill", "historical", "sports"] 
    base_url = "https://comic.naver.com/webtoon/genre?genre={}"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))

    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_without_cookie(shared_dict, url_list, genre_list)
    shared_dict_copy = shared_dict.copy()
    
    # get date from daily page
    driver = driver_set()
    get_url_untill_done(driver, "https://comic.naver.com/webtoon/weekday")
    daily_elements = driver.find_elements(By.CSS_SELECTOR, ".thumb")
    
    
    for daily_element in daily_elements:
        str_temp = daily_element.find_element(By.XPATH, "following-sibling::a").get_attribute("href")
        id_temp = str_temp[str_temp.index("titleId=") + 8 : str_temp.index("&")] 
        if id_temp in shared_dict_copy:
            day_temp = str_temp[str_temp.index("weekday=") + 8 : ]
            if day_temp == "mon":
                day_temp = "월"
            elif day_temp == "tue":
                day_temp = "화"
            elif day_temp == "wed":
                day_temp = "수"
            elif day_temp == "thu":
                day_temp = "목"
            elif day_temp == "fri":
                day_temp = "금"
            elif day_temp == "sat":
                day_temp = "토"
            elif day_temp == "sun":
                day_temp = "일"
            else:
                print("something wrong")
            if shared_dict_copy[id_temp][6] == "완결":
                item_finish_status = "연재"
                shared_dict_copy[id_temp][6] = day_temp             
            else:
                shared_dict_copy[id_temp][6] += "," 
                shared_dict_copy[id_temp][6] += day_temp 
    
    json.dump(shared_dict_copy, file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
    

   