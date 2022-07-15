from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager
import mysql.connector
import datetime

def collect_webtoon_data_cookie(shared_dict, url, genre_tag, cookie_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_elements_url = []

    # login with cookie 
    driver = driver_set()
    # get_url_untill_done(driver, "https://onestory.co.kr/member/login?redirectUri=%2F")
    # for cookie in cookie_list:
    #     driver.add_cookie(cookie)
    
    # click item
    for i in range(2):
        get_url_untill_done(driver, url)
        webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='ListItem']")
        driver.implicitly_wait(0.3)
        item_adult = webtoon_elements[i].find_elements(By.XPATH, ".//div[@class='ThumbnailBottomPlus19']")
        if len(item_adult) == 0:
            item_adult = False
        else:
            item_adult = True            
            
        driver.implicitly_wait(10)
        time.sleep(2)
        webtoon_elements[i].click()
        time.sleep(2)
        item_address = driver.current_url
        shared_dict.update(get_element_data(driver, item_address, genre_tag, i, item_adult))
    
    driver.close()
    return shared_dict
    
    
def get_element_data(driver, item_address, item_genre, i, item_adult):
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
    
    webtoon_data_dict[item_id] = [item_id, item_genre, item_address, item_rank, item_thumbnail, item_title, 
                                    item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

def multip_cookie(shared_dict, url_list, genre_list, cookie_list):
    pool = Pool(1) 
    for i in range(len(url_list)):  
        pool.apply_async(collect_webtoon_data_cookie, args =(shared_dict, url_list[i], genre_list[i], cookie_list))
        time.sleep(random.uniform(0.7,1.5))
    pool.close()
    pool.join()     
    



###########################################################################
if __name__ == '__main__':
       
    # get login cookies
    # driver = driver_set()
    
    # url = "https://www.bomtoon.com/comic/ep_list/100CleanUp/?p_id=tw1590"
    
    # get_url_untill_done(driver, url)
    # # item_synopsis = driver.find_element(By.ID, "comic_desc").text
    # print(driver.find_element(By.ID, "comic_desc").text)
    dict_temp = {}
    dict_temp1 = {'1' : ['1', 'romance', 'hi', '1'],
                  '2' : ['2', 'bl', 'hlee', '5']}
    dict_temp2 = {'2' : ['2', 'romance', 'hleo', '4'], 
                  '3' : ['3', 'gl', 'sd', '6'], }
    # for i in dict_temp.keys():
    #     if 
    
    arr = [1,2,3,4]
    
    print(arr[5])

    