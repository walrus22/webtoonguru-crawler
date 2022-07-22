from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list):
    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://onestory.co.kr/member/login?redirectUri=%2F")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    
    # click item
    for i in range(20): # number of item
        get_url_untill_done(driver, url, 0.7, 1.5)
        webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='ListItem']")
        driver.implicitly_wait(0.3)
        item_adult = webtoon_elements[i].find_elements(By.XPATH, ".//div[@class='ThumbnailBottomPlus19']")
        if len(item_adult) == 0:
            item_adult = False
        else:
            item_adult = True            
        driver.implicitly_wait(10)
        time.sleep(1)
        webtoon_elements[i].click()
        time.sleep(0.5)
        item_address = driver.current_url
        catch_duplicate(get_element_data(driver, item_address, genre_tag, i, item_adult), shared_dict)
        
    driver.close()
    return shared_dict
    
    
def get_element_data(driver, item_address, item_genre, i, item_adult):
    webtoon_data_dict = {}
    item_rank = i+1
    item_id = item_address[item_address.rfind("/")+1:]
    time.sleep(2)
    item_thumbnail = driver.find_element(By.XPATH, "//div[@class='ThumbnailInner']/img").get_attribute("src")
    item_title = driver.find_element(By.XPATH, "//span[@class='textSt tST18B tDark tDetailTopTextTitle']").text
    item_date = "None"
    item_finish_status = driver.find_element(By.XPATH, "//span[@class='textSt tB14 tMedium tEllipsis DetailTopTextEpisode']").text
    if item_finish_status.find("완결") != -1:
        item_finish_status = "완결"
    else:
        item_finish_status = "연재"
    item_synopsis = "None"
    item_artist = driver.find_element(By.XPATH, "//span[@class='textSt tB14 tMedium tEllipsis DetailTopTextArtist']").text
    
    insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult)
    
    return webtoon_data_dict

###########################################################################
if __name__ == '__main__':
    start = time.time()

    ### get login cookies
    driver = driver_set()
    get_url_untill_done(driver, "https://onestory.co.kr/member/login?redirectUri=%2F")
    driver.find_element(By.XPATH, "//div[@class='MemberLoginListItem facebook']/a").click()
    time.sleep(2)
    user_id = "tpa74231@gmail.com"
    user_pw = "Fortest111!!!"
    id_tag = "//input[@id='email']"
    pw_tag = "//input[@id='pass']"
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    ### main
    genre_list = ["26002", "26009", "26003", "26006", "26005", "26007", "26001", "26004","26011"] 
    genre_name = ["romance", "bl", "drama", "action", "fantasy", "daily", "gag", "thrill","adult"] 
    # genre_list = ["26002", "26009", "26003"]
    # genre_name = ["romance", "bl", "drama"] # dict으로 만들어도 될것같은데 {genre_list : genre_name..}
    base_url = "https://onestory.co.kr/display/rank/webtoon/DP{}?title=%EC%9B%B9%ED%88%B0%20%EB%9E%AD%ED%82%B9"
    shared_dict_copy = collect_multiprocessing(1, collect_webtoon_data, base_url, genre_list, cookie_list, genre_name=genre_name)
    save_as_json(os.getcwd(), Path(__file__).stem, shared_dict_copy, start)
    
    
