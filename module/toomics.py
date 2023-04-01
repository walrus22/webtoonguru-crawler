from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager
import requests

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, cookie_list, adult):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://www.toomics.com/ko")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, "https://www.toomics.com/ko")
    
    # change adult mode
    if adult == False:
        driver.find_element(By.XPATH,"//li[@class='mode1'] | //li[@class='mode1 active']").click()
    else:
        driver.find_element(By.XPATH,"//li[@class='mode3'] | //li[@class='mode3 active']").click()
        
    # collect item url    
    get_url_untill_done(driver, url)
    webtoon_elements = driver.find_elements(By.XPATH, "//li[@class='grid__li']") # webtoon element selection. 
    time.sleep(1)
    for element in webtoon_elements:
        item_address_temp = element.find_element(By.XPATH, "./a").get_attribute("href")
        webtoon_elements_url.append("https://www.toomics.com/webtoon/episode/toon/" + item_address_temp[item_address_temp.rfind("/")+1:])
    
    
    
    # 22.8.6 unify genre 
    if genre_tag == "school/action":
        genre_tag = ["school", "action"]
        
    if adult == True:
        if genre_tag == "ssul":
            genre_tag = "erotic"
        else:
            genre_tag = ["erotic"] + list(genre_tag.split())
            
    ### 7.21 avoid duplication
    catch_duplicate(get_element_data(driver, webtoon_elements_url, genre_tag, adult), shared_dict)
    driver.close()
    return 

def get_element_data(driver, webtoon_elements_url, item_genre, adult):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        get_url_untill_done(driver, item_address, 1, 2)
        item_rank += 1
        item_id = item_address[item_address.rfind("/")+1:]
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='episode__thumbnail']/img").get_attribute("src")
        
        item_title = driver.find_element(By.XPATH, "//h2[@class='episode__title']").text.replace(" ", "")
        item_date_list = driver.find_elements(By.XPATH, "//span[@class='episode__tags']/a")
        item_date = ""
        for item_date_element in item_date_list:
            if item_date_element.text.find("완결") != -1:
                item_date = "완결"
                item_finish_status = "완결"
                break
            elif item_date_element.text.find("요연재") != -1:
                item_date += item_date_element.text
        if item_date != "완결":
            item_date, item_finish_status = find_date(item_date, end_comment="완결", day_keyword=False, daylist_more=[])
            
        item_synopsis = driver.find_element(By.XPATH, "//div[@class='episode__summary']").text
        item_artist = driver.find_element(By.XPATH, "//dl[@class='episode__author']/dd").text.split("/")
        item_adult = adult
        
        if item_synopsis.find("+ 더보기") != -1:
            item_synopsis = item_synopsis[:item_synopsis.find("+ 더보기")]
        
        insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult) 
        
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, cookie_list, adult):
    pool = Pool(1) # prevent 403
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list, adult))
        time.sleep(random.uniform(0.7,1.5))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    
    # get login cookies
    driver = driver_set()
    get_url_untill_done(driver, "https://www.toomics.com/ko")
    driver.find_element(By.XPATH, "//a[@class='header__login']").click()
    time.sleep(1)
    user_id = os.environ['CRAWLER_ID']
    user_pw = os.environ['CRAWLER_PW']
    id_tag = "//input[@id='user_id']"
    pw_tag = "//input[@id='user_pw']"
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    base_url = "https://www.toomics.com/webtoon/top100/genre/{}"
    genre_list = ["8", "1066", "5", "1065", "2570", "1444", "1443", "1441", "7"]
    genre_name = ["school/action", "fantasy", "drama", "romance", "gag", "sports", "historical", "thrill+horror", "bl"] 
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
    multip_cookie(shared_dict, url_list, genre_name, cookie_list, adult=False) # choose one

    # collect item for adult site
    genre_list = ["5", "1065", "1066", "6", "1441", "1444", "7"]  #학원/액션, 개그 없음
    genre_name = ["drama", "romance", "fantasy", "ssul",  "thrill+horror", "sports","bl"] 
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
    multip_cookie(shared_dict, url_list, genre_name, cookie_list, adult=True) 
    shared_dict_copy = shared_dict.copy()    
    
    # store json
    save_as_json(os.getcwd(), Path(__file__).stem, shared_dict_copy, start)
