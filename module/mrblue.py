from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

################################# function setting ############################
def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = [] 
    
    # login cookie
    driver = driver_set()
    get_url_untill_done(driver, "https://www.mrblue.com/login?returnUrl=%2F")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # collect item url 
    webtoon_elements = driver.find_elements(By.CLASS_NAME, "img") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    ### 7.14 avoid duplicate
    webtoon_data_dict_temp = get_element_data(driver, webtoon_elements_url, genre_tag)
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
    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url:
        get_url_untill_done(driver, item_address)
        item_id = item_address[item_address.rfind("/")+1:]
        item_rank += 1
        
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='img-box']/p/img").get_attribute("src")
        item_title = driver.find_element(By.CLASS_NAME, 'title').text
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[1]").text, "완결", False)
        item_synopsis = driver.find_element(By.XPATH, "//div[@class='txt-box']/p/span").text
        if driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[3]").text.find("19세") == -1:
            item_adult = False
        else: 
            item_adult = True
        
        # 그림/글 : 1명 // 그림 ~명 글 ~명 2가지 케이스 있다
        item_artist = ""
        first = True
        for author in driver.find_elements(By.XPATH, "//span[@class='authorname long'] | //span[@class='authorname']"):
            author = author.text
            if first == True:
                first = False
            else:
                item_artist += ","
            item_artist += author
        
        item_synopsis = item_synopsis.replace("'", "\\'")
        item_artist = item_artist.replace("'", "\\'")
        item_title = item_title.replace("'", "\\'")
        
        webtoon_data_dict[item_id] = [item_id, [item_genre], item_address, [item_rank], item_thumbnail, item_title, 
                                    item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(2) 
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()     
################################################################################

if __name__ == '__main__':
    start = time.time()
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')
    
    genre_list = ["romance", "bl", "erotic", "drama", "gl", "action", "fantasy", "thriller"] 
    url_list=[]
    base_url = "https://www.mrblue.com/webtoon/genre/{}?sortby=rank"
    for u in genre_list:
        url_list.append(base_url.format(u))

    #login session
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    driver = driver_set()
    get_url_untill_done(driver, "https://www.mrblue.com/login?returnUrl=%2F")
    login_for_adult(driver, user_id, user_pw, "//input[@id='pu-page-id']","//input[@id='pu-page-pw']")
    cookie_list = driver.get_cookies()
    driver.close()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip(shared_dict, url_list, genre_list, cookie_list)
    shared_dict_copy = shared_dict.copy()
    
    # store json
    file = open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w")
    json.dump(shared_dict_copy, file, separators=(',', ':'))
    file.close()
    
    # # store in mongodb 
    # collection_name = Path(__file__).stem + now
    # mydb = my_mongodb("webtoon_db"+ now)
    # mydb_collection = mydb.db[collection_name]    
    # mydb_collection.insert_many(mydb.convert_to_list(shared_dict_copy))
    # print("{} >> ".format(Path(__file__).stem), time.time() - start)   

    
