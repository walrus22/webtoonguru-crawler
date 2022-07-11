from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://onestory.co.kr/member/login?redirectUri=%2F")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # collect item url    
    webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='ListItem']") # webtoon element selection. 
    print(len(webtoon_elements)) # for check
    for i in range(len(webtoon_elements)):
        webtoon_elements[i].click()
        item_address = driver.current_url
        shared_dict.update(get_element_data(driver, item_address, genre_tag, i))
        get_url_untill_done(driver, url)
        
    # for element in webtoon_elements:
    #     webtoon_elements_url.append(element.find_element(By.XPATH, "Your_elemet_URL_Path //[@class='']").get_attribute("href"))
    
    driver.close()
    return shared_dict
    
    
def get_element_data(driver, item_address, genre_tag, i):
    webtoon_data_dict = {}
    item_rank = i+1
    item_id = item_address[item_address.rfind("/")+1:]
    
    item_thumbnail = driver.find_element(By.XPATH, "//div[@class='ThumbnailInner']/img").get_attribute("src")
    item_title = driver.find_element(By.XPATH, "//span[@class='textSt tST18B tDark tDetailTopTextTitle']").text
    # item_date, item_finish_status = find_date(item_date_temp=driver.find_element(By.XPATH, ""), end_comment= , day_keyword=, daylist_more=)
    item_date = "None"
    item_finish_status = driver.find_element(By.XPATH, "//span[@class='textSt tB14 tMedium tEllipsis DetailTopTextEpisode']").text
    if item_finish_status.find("완결") != -1:
        item_finish_status = "완결"
    else:
        item_finish_status = "연재"
        
    item_synopsis = "None"
    item_artist = driver.find_element(By.XPATH, "//span[@class='textSt tB14 tMedium tEllipsis DetailTopTextArtist']").text
    if genre_tag == "adult" :
        item_adult = True
    else:
        item_adult = False
    webtoon_data_dict[item_id] = [item_id, genre_tag, item_address, item_rank, item_thumbnail, item_title, 
                                    item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(len(url_list)) 
    for i in range(1):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
    pool.close()
    pool.join()     

###########################################################################
if __name__ == '__main__':
    start = time.time()
    file = open(os.path.join(os.getcwd(), "json", "{}.json".format(Path(__file__).stem)), "w")
    genre_list = ["26002", "26009", "26003", "26006", "26005", "26007", "26001", "26004","26011"] 
    genre_name = ["romance", "bl", "drama", "action", "fantasy", "daily", "gag", "thrill","adult"] # 성인을 맨뒤로 놔서, 중복있는 경우 adult=true
    base_url = "https://onestory.co.kr/display/rank/webtoon/DP{}?title=%EC%9B%B9%ED%88%B0%20%EB%9E%AD%ED%82%B9"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    driver = driver_set()
    get_url_untill_done(driver, "https://onestory.co.kr/member/login?redirectUri=%2F")
    driver.find_element(By.XPATH, "//div[@class='MemberLoginListItem facebook']/a").click()
    time.sleep(3)
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    id_tag = "//input[@id='email']"
    pw_tag = "//input[@id='pass']"
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    manager = Manager()
    shared_dict = manager.dict()
    multip_cookie(shared_dict, url_list, genre_name, cookie_list) # choose one
    multip_without_cookie(shared_dict, url_list, genre_list)
    shared_dict_copy = shared_dict.copy()
    json.dump(shared_dict_copy, file, separators=(',', ':'))
    print("time :", time.time() - start)    
    file.close()
    
