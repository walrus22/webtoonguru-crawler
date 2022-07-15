from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager
import  requests



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
    
    ### 7.14 avoid duplicate
    webtoon_data_dict_temp = get_element_data(driver, webtoon_elements_url, genre_tag, adult)
    for i in list(webtoon_data_dict_temp):
        if i in shared_dict.keys():
            shared_temp = shared_dict[i]
            shared_temp[1]+= (webtoon_data_dict_temp[i][1]) # genre
            shared_temp[3]+= (webtoon_data_dict_temp[i][3]) # rank
            shared_dict[i] = shared_temp
            webtoon_data_dict_temp.pop(i)   
    shared_dict.update(webtoon_data_dict_temp)
    driver.close()
    return 

def get_element_data(driver, webtoon_elements_url, item_genre, adult):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
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
        item_artist = driver.find_element(By.XPATH, "//dl[@class='episode__author']/dd").text.replace("/",",")
        item_adult = adult
        
        item_synopsis = item_synopsis.replace("'", "\\'")
        item_artist = item_artist.replace("'", "\\'")
        item_title = item_title.replace("'", "\\'")
        
        if item_synopsis.find("+ 더보기") != -1:
            item_synopsis = item_synopsis[:item_synopsis.find("+ 더보기")]
        
        webtoon_data_dict[item_id] = [item_id, [item_genre], item_address, [item_rank], item_thumbnail, item_title, 
                                      item_date, item_finish_status, item_synopsis, item_artist, item_adult]
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
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')
    genre_list = ["8", "1066", "5", "1065", "2570", "1444", "1443", "1441", "7"]
    genre_name = ["school/action", "fantasy", "drama", "romance", "gag", "sports", "historical", "horror/thrill", "bl"] 
    base_url = "https://www.toomics.com/webtoon/top100/genre/{}"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    driver = driver_set()
    get_url_untill_done(driver, "https://www.toomics.com/ko")
    driver.find_element(By.XPATH, "//a[@class='header__login']").click()
    time.sleep(1)
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    id_tag = "//input[@id='user_id']"
    pw_tag = "//input[@id='user_pw']"
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_name, cookie_list, adult=False) # choose one

    # collect item for adult site
    genre_list = ["5", "1065", "1066", "6", "1441", "1444", "7"]  #학원/액션, 개그 없음
    genre_name = ["drama", "romance", "fantasy", "ssul",  "horror/thrill", "sports","bl"] 
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
    multip_cookie(shared_dict, url_list, genre_name, cookie_list, adult=True) 
    shared_dict_copy = shared_dict.copy()    
    
    # store in mongodb 
    collection_name = Path(__file__).stem + now
    mydb = my_mongodb("webtoon_db"+ now)
    mydb_collection = mydb.db[collection_name]    
    mydb_collection.insert_many(mydb.convert_to_list(shared_dict_copy))
    print("{} >> ".format(Path(__file__).stem), time.time() - start)   

