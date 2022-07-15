from collector_setting import *
import json
import pickle
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_cookie(shared_dict, url, genre_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie
    driver = driver_set()
    get_url_untill_done(driver, "https://page.kakao.com/main")
    cookie_list = pickle.load(open(os.path.join(os.getcwd(), "module", "cookies", "{}_cookie.pkl".format(Path(__file__).stem)), "rb"))
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)   
    
    # click see more button
    driver.find_element(By.XPATH, "//div[@class='css-hg8e5']/div/div[2]/a").click()
    time.sleep(1)
    
    # collect item url   
    webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='css-j3o65g']/a") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.get_attribute("href"))
    driver.implicitly_wait(30)
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    driver.close()
    return shared_dict  
    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        item_rank += 1
        item_id = item_address[item_address.rfind("=")+1:]
        item_thumbnail = driver.find_element(By.XPATH, "//img[@class='css-1ithwm4']").get_attribute("src")
        item_title = driver.find_element(By.XPATH, "//h2[@class='text-ellipsis css-jgjrt']").text
        item_date, item_finish_status = find_date(driver.find_elements(By.XPATH, "//div[@class='text-ellipsis css-7a7cma']")[0].text, end_comment= "완결", day_keyword=False, daylist_more=[])
        item_artist = driver.find_elements(By.XPATH, "//div[@class='text-ellipsis css-7a7cma']")[1].text
        
        # click detail button
        driver.find_element(By.XPATH, "//button[@data-key='isDescriptionOpen']").click()
        time.sleep(0.5)
        item_synopsis = driver.find_element(By.XPATH, "//div[@class='jsx-3755015728 descriptionBox descriptionBox_pc  lineHeight']").text
        item_adult = False # 카카오 페이지는 성인물 없나봄
        
        item_synopsis = item_synopsis.replace("'", "\\'")
        item_artist = item_artist.replace("'", "\\'")
        item_title = item_title.replace("'", "\\'")
        
        webtoon_data_dict[item_id] = [item_id, item_genre, item_address, item_rank, item_thumbnail, item_title, 
                                      item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_name):
    pool = Pool(1) # kakao 멀티프로세싱 x
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_name[i]))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    # file = open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w")
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')
    table_name = Path(__file__).stem + now
    
    genre_list = ["115", "116", "121", "69", "112", "119"] 
    genre_name = ["fantasy", "drama", "romance", "romance+fantasy", "historical", "bl"]  # 소년 = fantasy
    
    base_url = "https://page.kakao.com/main?categoryUid=10&subCategoryUid={}"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    ### MANUALLY
    ### get login session cookie 
    # driver = driver_set()
    # get_url_untill_done(driver, "https://page.kakao.com/main")
    # time.sleep(50) # time for login
    # cookie_list = driver.get_cookies()
    # pickle.dump(cookie_list, open(os.path.join(os.getcwd(), "module", "cookies", "{}_cookie.pkl".format(Path(__file__).stem)),"wb"))     
    # driver.close()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_name)
    shared_dict_copy = shared_dict.copy()
    # json.dump(shared_dict_copy, file, separators=(',', ':'))
    mydb = mysql_db("webtoon_db"+ now)
    mydb.create_table(table_name)
    for dict_value in shared_dict_copy.values():
        mydb.insert_to_mysql(dict_value, table_name)
    mydb.db.commit()
    
    print("{} >> ".format(Path(__file__).stem), time.time() - start)
    # file.close()
    
