from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "LOGIN_URL")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # collect item url    
    webtoon_elements = driver.find_elements(By.XPATH, "Your_Element_tag") # webtoon element selection. 
    print(len(webtoon_elements)) # for check
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "Your_elemet_URL_Path").get_attribute("href"))
    
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    driver.close()
    return shared_dict
    

def collect_webtoon_data_without_cookie(shared_dict, url, genre_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []
    
    # collect item url    
    driver = driver_set()
    get_url_untill_done(driver, url)
    webtoon_elements = driver.find_elements(By.XPATH, "Your_element_tag") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "Your_elemet_URL_Path").get_attribute("href"))
    
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    driver.close()
    return shared_dict
        
    
def get_element_data(driver, webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        item_rank += 1
        # item_rank = webtoon_elements[i].find_element(By.XPATH, "") # choose one
        
        item_id = driver.find_element(By.XPATH, "")
        item_id = item_address[:]
        item_id = item_address[item_address.rfind("/")+1:]
        
        item_thumbnail = driver.find_element(By.XPATH, "")
        item_title = driver.find_element(By.XPATH, "")
        item_date, item_finish_status = find_date(item_date_temp=driver.find_element(By.XPATH, ""), end_comment= , day_keyword=, daylist_more=)
        # item_date = 
        # item_finish_status = driver.find_element(By.XPATH, "")
        item_synopsis = driver.find_element(By.XPATH, "")
        item_artist = driver.find_element(By.XPATH, "")
        item_adult = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [item_id, genre_tag, item_address, item_rank, item_thumbnail, item_title, 
                                      item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(len(url_list)) 
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()     

def multip_without_cookie(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(len(url_list)) 
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_without_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "json", "{}.json".format(Path(__file__).stem)), "w")
    genre_list = ["", "", "", "", "", "", "", "", "", ""] 
    base_url = ""
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    user_id = ""
    user_pw = ""
    id_tag = "//input[@='']"
    pw_tag = "//input[@='']"
    driver = driver_set()
    get_url_untill_done(driver, "LOGIN_PAGE_URL")
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_list, cookie_list) # choose one
    multip_without_cookie(shared_dict, url_list, genre_list)
    json.dump(shared_dict.copy(), file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
    
