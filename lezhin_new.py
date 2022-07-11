from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://www.lezhin.com/ko/login?redirect=%2Fko#email")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # 19 button click
    driver.find_element(By.XPATH, "//span[@class='contentMode supports__item']").click()
    
    # collect item url    
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, ".lzComic__item") # webtoon element selection. 
    print(len(webtoon_elements)) # for check
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    driver.close()
    return shared_dict       
    
def get_element_data(driver, webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)™
        item_rank += 1
        item_id = item_address[item_address.rfind("/")+1:]
        item_thumbnail = driver.find_element(By.XPATH, "//picture[@class='comicInfo__cover']/source").get_attribute("srcset")
        item_title = driver.find_element(By.CSS_SELECTOR, ".comicInfo__title").text
        # item_date = 레진 안나와
        # item_finish_status = 이거도 안나옴 ㅡㅡ;
        item_date = "None"
        item_finish_status = "None"
        item_artist = driver.find_element(By.XPATH, "")
        item_adult = driver.find_element(By.XPATH, "//span[@class='comicInfo__rating']").text
        if item_adult.find("19세") != -1: # adult
            item_adult = True
        else:
            item_adult = False
        item_synopsis = ""
        item_synopsis_list = driver.find_elements(By.XPATH, "//div[@class='comicInfoExtend__synopsis']/p")
        for i in len(item_synopsis_list):
            if i == 0:
                item_synopsis += item_synopsis_list[i]
            else:
                item_synopsis += "\n"
                item_synopsis += item_synopsis_list[i]          
            
        webtoon_data_dict[item_id] = [item_id, genre_tag, item_address, item_rank, item_thumbnail, 
                                      item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(1) 
    for i in range(1):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()       

###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "json", "{}.json".format(Path(__file__).stem)), "w")
    genre_list = ["romance", "bl", "drama", "fantasy", "gag", "action", "school", "mystery", "day", "gl"] # 사이트별 설정 
    base_url = "https://www.lezhin.com/ko/ranking/detail?genre={}&type=realtime"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    id_tag = "//input[@name='username']"
    pw_tag = "//input[@name='password']"
    driver = driver_set()
    get_url_untill_done(driver, "https://www.lezhin.com/ko/login?redirect=%2Fko#email")
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_list, cookie_list) # choose one
    json.dump(shared_dict.copy(), file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
    


