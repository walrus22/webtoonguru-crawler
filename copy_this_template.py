from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager


### After kakao new, 그냥 url만 주고 하나씩 접속해서 따는게 낫겠다. 굳이 앞에서 이것저것 따올필요가 없었네;;
def collect_webtoon_data(base_url, genre_list, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # collect item url    
    for genre_tag in genre_list:
        url = base_url.format(genre_tag)
        get_url_untill_done(driver, url)
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        for element in webtoon_elements:
            webtoon_elements_url.append(element.get_attribute("href"))
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        
        item_id = driver.find_element(By.XPATH, "")
        item_id = item_address[:]
        item_id = item_address[item_address.rfind("/")+1:]
        
        item_rank += 1
        # item_rank = webtoon_elements[i].find_element(By.XPATH, "") # choose one
        item_thumbnail = driver.find_element(By.XPATH, "")
        item_title = driver.find_element(By.XPATH, "")
        item_date, item_finish_status = find_date(item_date_temp=driver.find_element(By.XPATH, ""), end_comment= , day_keyword=, daylist_more=)
        item_synopsis = driver.find_element(By.XPATH, "")
        item_artist = driver.find_element(By.XPATH, "")
        item_etc_status = driver.find_element(By.XPATH, "")
        item_adult = 
        # item_date = 
        # item_finish_status = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [genre_tag, item_id, item_address, item_rank, item_thumbnail, 
                                      item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(len(url_list)) #
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "json", "{}.json".format(Path(__file__).stem)), "w")
    
    genre_list = ["",] # 사이트별 설정 
    base_url = ""
    css_tag = ""

    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    #login session
    user_id = ""
    user_pw = ""
    driver = driver_set()
    get_url_untill_done(driver, "")
    login_for_adult(driver, user_id, user_pw, "//input[@id='pu-page-id']","//input[@id='pu-page-pw']")
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    manager = Manager()
    shared_dict = manager.dict()
    # multip(url_list, cookie_list) 
    multip(shared_dict, url_list, genre_list, cookie_list)
    json.dump(shared_dict.copy(), file, separators=(',', ':'))
    
    # json.dump(shared_dict, file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
