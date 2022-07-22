from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list):
    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://www.lezhin.com/ko/login?redirect=%2Fko#email")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)
    
    # 19 button click
    driver.find_element(By.XPATH, "//span[@class='contentMode supports__item']").click()
    
    # collect item url    
    webtoon_elements_url = []
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, ".lzComic__item") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    # webtoon_elements_url = webtoon_elements_url[:3]
    
    ### 7.21 avoid duplicate
    catch_duplicate(get_element_data(driver, webtoon_elements_url, genre_tag), shared_dict)
    driver.close()
    return  
    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        get_url_untill_done(driver, item_address,0,0)
        item_rank += 1
        item_id = item_address[item_address.rfind("/")+1:]
        item_thumbnail = driver.find_element(By.XPATH, "//picture[@class='comicInfo__cover']/source").get_attribute("srcset")
        item_title = driver.find_element(By.CSS_SELECTOR, ".comicInfo__title").text
        # item_date = 레진 안나와
        # item_finish_status = 이거도 안나옴 ㅡㅡ;
        item_date = "None"
        item_finish_status = "None"
        
        item_artist_list = driver.find_elements(By.XPATH, "//div[@class='comicInfo__artist']/a")
        # time.sleep(0.2)
        for i in range(len(item_artist_list)):
            if i == 0 :
                item_artist = item_artist_list[i].text
            else : 
                item_artist += "," + item_artist_list[i].text
        
        item_adult = driver.find_element(By.XPATH, "//span[@class='comicInfo__rating']").text
        if item_adult.find("19세") != -1: # adult
            item_adult = True
        else:
            item_adult = False
            
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//button[@class='comicInfo__btnShowExtend']").click()
        # item_synopsis = driver.find_element(By.XPATH, "//div[@class='comicInfoExtend__synopsis']/p").text
        item_synopsis_list = driver.find_elements(By.XPATH, "//div[@class='comicInfoExtend__synopsis']/p")
        for i in range(len(item_synopsis_list)):
            if i == 0:
                item_synopsis = item_synopsis_list[i].text
            else:
                item_synopsis += "\n" + item_synopsis_list[i].text 
        insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult)
        
    return webtoon_data_dict
###########################################################################
if __name__ == '__main__':
    start = time.time()
    

    driver = driver_set()
    item_address = "https://www.lezhin.com/ko/comic/monthly_gl"
    get_url_untill_done(driver,item_address ,0,0)
###

    item_thumbnail = driver.find_element(By.XPATH, "//picture[@class='comicInfo__cover']/source").get_attribute("srcset")
    item_title = driver.find_element(By.CSS_SELECTOR, ".comicInfo__title").text
    # item_date = 레진 안나와
    # item_finish_status = 이거도 안나옴 ㅡㅡ;
    item_date = "None"
    item_finish_status = "None"
    
    item_artist_list = driver.find_elements(By.XPATH, "//div[@class='comicInfo__artist']/a")
    time.sleep(0.5)
    for i in range(len(item_artist_list)):
        if i == 0 :
            item_artist = item_artist_list[i].text
        else : 
            item_artist += "," + item_artist_list[i].text
    
    item_adult = driver.find_element(By.XPATH, "//span[@class='comicInfo__rating']").text
    if item_adult.find("19세") != -1: # adult
        item_adult = True
    else:
        item_adult = False

    buttontemp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='comicInfo__btnShowExtend']")))
    buttontemp.click()

    # driver.find_element(By.XPATH, "//button[@class='comicInfo__btnShowExtend']").click()
    # time.sleep(0.8)
    
    
    item_synopsis_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='comicInfoExtend__synopsis']")))
    item_synopsis_list = item_synopsis_list.find_elements(By.XPATH, "./p")
    
    # item_synopsis_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='comicInfoExtend__synopsis']/p")))    
    
    # item_synopsis_list = driver.find_elements(By.XPATH, "//div[@class='comicInfoExtend__synopsis']/p")
    
    for i in range(len(item_synopsis_list)):
        if i == 0:
            item_synopsis = item_synopsis_list[i].text
        else:
            item_synopsis += "\n" + item_synopsis_list[i].text 
    
    print(item_synopsis)
    print("hi" + str(1))