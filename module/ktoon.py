from collector_setting import *
import json
from pathlib import Path
from multiprocessing import Pool, Manager

def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list):
    # login with cookie 
    driver = driver_set()
    get_url_untill_done(driver, "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq=100#")
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url) # 버튼 자동으로 바뀌네
    
    # 다음 페이지 있으면 탐색 
    # while True:
    #     get_url_untill_done(driver, url)
    #     driver.implicitly_wait(2)
    #     next_page_element = driver.find_elements(By.CLASS_NAME, "next")
    #     if len(next_page_element) == 0:
    #         break
    #     else: 
    #         # driver.implicitly_wait(300)
    #         rank_basis+=len(webtoon_elements)
    #         url = next_page_element[0].find_element(By.XPATH, "./a").get_attribute("href")
    #         get_url_untill_done(driver, url)
    #         driver.implicitly_wait(2)
    #         if len(driver.find_elements(By.CLASS_NAME, "tm7")) == 0: # there is next page but no elements
    #             break
    #         webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection.         
    #         webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag, rank_basis))    
    
    # 22.8.6 unify genre 
    if genre_tag == "fantasy/SF":
        genre_tag = "fantasy"
    elif genre_tag == "bl/gl":
        genre_tag = ["bl", "gl"]
    elif genre_tag == "thrill/horror":
        genre_tag = "thrill+horror"
    
    # collect item url  
    webtoon_elements_url = []
    webtoon_elements = driver.find_elements(By.XPATH, "//li[@class='tm7']") # webtoon element selection. 
    for element in webtoon_elements:
        webtoon_elements_url.append(element.find_element(By.XPATH, "./a").get_attribute("href"))
    
    ### 7.21 avoid duplicate
    catch_duplicate(get_element_data(driver, webtoon_elements_url, genre_tag), shared_dict)
    driver.close()
    return 
    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address, 0, 0)
        item_rank += 1
        item_id = item_address[item_address.rfind("=")+1:]
        
        item_thumbnail = driver.find_element(By.XPATH, "//span[@class='thmb']/img").get_attribute("src")
        item_title = driver.find_element(By.XPATH, "//h3[@class='hc']").text
        item_synopsis = driver.find_element(By.XPATH, "//p[@class='toon_copy']").text
        item_date, item_finish_status = find_date(driver.find_elements(By.XPATH, "//p[@class='toon_author']/span")[-2].text, "완료", True)
        
        artist_list = driver.find_elements(By.CLASS_NAME, "authorInfoBtn")                
        item_artist = []
        for i in artist_list:
            item_artist.append(i.text)
    
        if item_title.find("19세이상") != -1:
            item_adult = True
            item_title = item_title[:item_title.find("19세이상") ]
        else:
            item_adult = False
        
        if item_title.find("세이상") != -1:
            item_title = item_title[:-5]        
            
        insert_data(webtoon_data_dict,item_id,item_genre,item_address,item_rank,item_thumbnail,item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult)
    return webtoon_data_dict


###########################################################################
if __name__ == '__main__':
    start = time.time()
    genre_list = ["123", "118", "3", "5", "1", "6", "8", "16", "109", "113"] # 로맨스, bl/gl, 개그, 드라마, 일상, 판타지/SF, 감성, 액션, 스릴러/공포, 학원
    genre_name = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
    base_url = "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq={}"
    url_list=[]
    for u in genre_list:
        url_list.append(base_url.format(u))
        
    # get login cookies
    driver = driver_set()
    user_id = os.environ['CRAWLER_ID']
    user_pw = os.environ['CRAWLER_PW']
    id_tag = "//input[@id='useridWeb']"
    pw_tag = "//input[@id='passwdWeb']"
    get_url_untill_done(driver, "https://www.myktoon.com/web/webtoon/works_list.kt?genreseq=100#")
    
    # click adult button
    driver.find_element(By.XPATH, "//label[@class='check_changetext']").click()
    # headless 모드에서 Element is not clickable at point 발생하면 윈도우 사이즈를 설정해주면 됨.
    
    # save cookie 
    time.sleep(3)
    driver.find_element(By.XPATH, "//a[@class='btn_submit loginPrcBtn']").click()    
    login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
    cookie_list = driver.get_cookies()
    driver.close()
    driver.quit()
    
    # main
    shared_dict_copy = collect_multiprocessing(2, collect_webtoon_data, base_url, genre_list, cookie_list, genre_name)
    save_as_json(os.getcwd(), Path(__file__).stem, shared_dict_copy, start) 
    

