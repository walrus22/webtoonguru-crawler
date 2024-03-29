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
    time.sleep(1)
    
    # collect item url    
    webtoon_elements_url = []
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, ".lzComic__item") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    # 22.8.6 unify genre 
    if genre_tag == "day":
        genre_tag = "daily"
    elif genre_tag == "mystery":
        genre_tag = "thrill+horror"
    
    ### 7.21 avoid duplicate
    catch_duplicate(get_element_data(driver, webtoon_elements_url, genre_tag), shared_dict)
    driver.close()
    return  
    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    counter = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        get_url_untill_done(driver, item_address,0,0)
        item_rank += 1
        item_id = item_address[item_address.rfind("/")+1:]
        item_thumbnail = driver.find_element(By.XPATH, "//picture[@class='comicInfo__cover']/source").get_attribute("srcset")
        item_title = driver.find_element(By.CSS_SELECTOR, ".comicInfo__title").text
        # item_date = 레진 안나와
        # item_finish_status = 이거도 안나옴 ㅡㅡ;
        item_date = ""
        item_finish_status = ""
        
        item_artist_list = driver.find_elements(By.XPATH, "//div[@class='comicInfo__artist']/a")
        item_artist = []
        for i in item_artist_list:
            item_artist.append(i.text)

        item_adult = driver.find_element(By.XPATH, "//span[@class='comicInfo__rating']").text
        if item_adult.find("19세") != -1: # adult
            item_adult = True
        else:
            item_adult = False
            
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='comicInfo__btnShowExtend']"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@class='comicInfo__btnShowExtend']").click()
        time.sleep(2)
        driver.implicitly_wait(10)
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
    
    # get login cookies
    user_id = os.environ['CRAWLER_ID']
    user_pw = os.environ['CRAWLER_PW']
    id_tag = "//input[@name='username']"
    pw_tag = "//input[@name='password']"
    driver = driver_set()
    get_url_untill_done(driver, "https://www.lezhin.com/ko/login?redirect=%2Fko#email")
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    genre_list = ["romance", "bl", "drama", "fantasy", "gag", "action", "school", "mystery", "day", "gl"] # 사이트별 설정 
    base_url = "https://www.lezhin.com/ko/ranking/detail?genre={}&type=realtime"
    shared_dict_copy = collect_multiprocessing(10, collect_webtoon_data, base_url, genre_list, cookie_list) 
    
    # store json
    save_as_json(os.getcwd(), Path(__file__).stem, shared_dict_copy, start)
