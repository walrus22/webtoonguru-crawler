from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager
import re

################################# function setting ############################
def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list):
    # login cookie
    driver = driver_set()
    get_url_untill_done(driver, "https://www.mrblue.com/login?returnUrl=%2F")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # collect item url 
    webtoon_elements_url = [] 
    webtoon_elements = driver.find_elements(By.CLASS_NAME, "img") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    # 22.8.6 unify genre 
    if genre_tag == "thriller":
        genre_tag = "thrill+horror"
    
    ### 7.21 avoid duplicate
    catch_duplicate(get_element_data(driver, webtoon_elements_url, genre_tag), shared_dict)
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
        item_artist = []
        for author in driver.find_elements(By.XPATH, "//span[@class='authorname long'] | //span[@class='authorname']"):
            if author.text == "*9": # 8.7 *9 이거 regex 검색이 안되네.. 
                item_artist += ["9"]
            else:
                item_artist += re.split(r',\s*(?![^()]*\))', author.text)
            
            
        # item_artist = ""
        # first = True
        # for author in driver.find_elements(By.XPATH, "//span[@class='authorname long'] | //span[@class='authorname']"):
        #     author = author.text
        #     if first == True:
        #         first = False
        #     else:
        #         item_artist += ","
        #     item_artist += author
        
        insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult)
        
    return webtoon_data_dict
  
################################################################################
if __name__ == '__main__':
    start = time.time()

    #login session
    user_id = os.environ['CRAWLER_ID']
    user_pw = os.environ['CRAWLER_PW']
    driver = driver_set()
    get_url_untill_done(driver, "https://www.mrblue.com/login?returnUrl=%2F")
    login_for_adult(driver, user_id, user_pw, "//input[@id='pu-page-id']","//input[@id='pu-page-pw']")
    cookie_list = driver.get_cookies()
    driver.close()
    
    # main
    # genre_list = ["thriller"] 
    genre_list = ["romance", "bl", "erotic", "drama", "gl", "action", "fantasy", "thriller"] 
    base_url = "https://www.mrblue.com/webtoon/genre/{}?sortby=rank"
    shared_dict_copy = collect_multiprocessing(2, collect_webtoon_data, base_url, genre_list, cookie_list)
    
    # store json
    save_as_json(os.getcwd(), Path(__file__).stem, shared_dict_copy, start)
    

    
