from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, genre_name, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://www.bomtoon.com/")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # click all age
    driver.find_element(By.XPATH, "//div[@class='grade']/a").click()
    time.sleep(0.5)
    
    # click genre
    driver.find_element(By.XPATH, "//select[@class='arrow type']/option[@value='{}']".format(genre_tag)).click()
    time.sleep(0.5)
    
    # collect item url   
    webtoon_elements = driver.find_elements(By.XPATH, "//ul[@id='bt-rank-list']/li") # webtoon element selection. 
    for element in webtoon_elements:
        # 주소랑 성인여부 함께 보냄
        driver.implicitly_wait(0.3)
        if len(element.find_elements(By.XPATH, ".//div[@class='adult']")) == 0:
            item_adult = False
        else: 
            item_adult = True
        webtoon_elements_url.append([element.find_element(By.XPATH, "./a").get_attribute("href"), item_adult])
    
    webtoon_elements_url = webtoon_elements_url[:4]
    
    driver.implicitly_wait(30)
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_name))
    driver.close()
    return shared_dict
    
def get_element_data(driver, webtoon_elements_url, genre_name):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address[0])
        item_rank += 1
        item_id = item_address[0][item_address[0].rfind("/")+1:]
        
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='kv']/span").get_attribute("style")
        item_thumbnail = item_thumbnail[item_thumbnail.index('(')+3:-3]
        
        item_title = driver.find_element(By.XPATH, "//p[@id='bt-comic-name']").text
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='head']/span").text, "완결", True, ["열흘"])
        # item_date = 열흘말고도 있음?
        item_synopsis = driver.find_element(By.CSS_SELECTOR, "#comic_desc").text
        item_artist = driver.find_element(By.CLASS_NAME, "author").text.replace("&",",") # & -> ,
        item_adult = item_address[1]
        webtoon_data_dict[item_id] = [item_id, genre_name, item_address[0], item_rank, item_thumbnail, item_title, 
                                      item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, genre_name, cookie_list):
    pool = Pool(1) 
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], genre_name[i], cookie_list))
    pool.close()
    pool.join()     
###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w")
    genre_list = [4, 3] # 사이트별 설정 
    genre_name = ["bl", "romance"] 
    base_url = "https://www.bomtoon.com/main/rank"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    id_tag = "//input[@id='user_id']"
    pw_tag = "//input[@id='user_pw']"
    driver = driver_set()
    get_url_untill_done(driver, "https://www.bomtoon.com/")
    # time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "popCb")[1].click()
    # time.sleep(2)
    driver.find_element(By.CLASS_NAME, "btn-menu").click()
    # time.sleep(2)
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_list, genre_name, cookie_list)
    shared_dict_copy = shared_dict.copy()
    json.dump(shared_dict_copy, file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
    

