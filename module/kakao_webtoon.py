from collector_setting import *
import json
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
from multiprocessing import Pool, Manager
import pickle
from selenium.common.exceptions import WebDriverException



################################# function setting ############################
# https://stackoverflow.com/questions/47274852/mouse-scroll-wheel-with-selenium-webdriver-on-element-without-scrollbar/47287595#47287595
def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):
  error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }    
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
  if error:
    raise WebDriverException(error)

def collect_webtoon_data(shared_dict, url, genre_tag, counter):
# def collect_webtoon_data(shared_dict, url, genre_tag, cookie_list, counter):
    webtoon_elements_url = []
    
    # login with cookie
    driver = driver_set()
    get_url_untill_done(driver, "https://webtoon.kakao.com/")
    cookie_list = pickle.load(open(os.path.join(os.getcwd(), "module", "cookies", "{}_cookie.pkl".format(Path(__file__).stem)), "rb"))
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    get_url_untill_done(driver, url)   
    
    # click to move
    genre_click_list = driver.find_elements(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-bold-white light:text-black !whitespace-nowrap']")
    genre_click_list[counter].click()
    time.sleep(2)
    
    # collect item url
    webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='relative responsive-cell']/div/div/a") # webtoon element selection. 
    for elements in webtoon_elements:
        webtoon_elements_url.append(elements.get_attribute("href"))
    webtoon_elements_url.insert(0, driver.find_element(By.XPATH, "//a[@class='relative w-full h-full opacity-0 z-2 animate-fadeIn']").get_attribute("href"))
    shared_dict.update(get_element_data(driver, webtoon_elements_url, genre_tag))
    
    driver.close()
    return shared_dict

    
def get_element_data(driver, webtoon_elements_url, item_genre):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        item_id = item_address[item_address.rfind("/")+1:]
        item_rank += 1
        get_url_untill_done(driver, item_address, 2, 3 ) # s
        fore_temp = driver.find_elements(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/*")[0]
        if fore_temp.tag_name == "video":
            foreground = Image.open(urlopen(fore_temp.get_attribute("poster"))).convert("RGBA")
        else :
            foreground = Image.open(urlopen(fore_temp.find_element(By.XPATH, "./img").get_attribute("src"))).convert("RGBA")
        background = Image.open(urlopen(driver.find_element(By.XPATH, "//picture[@class='bg-content-home']/source").get_attribute("srcset"))).convert("RGBA")
        background.paste(foreground, (20, 150), foreground) # fore: 710x600 , back: 750x13??
        img = background.crop((0,0,750,750))
        img.save(os.path.join(os.getcwd(), "kakao_image", "{}.png".format(item_id))) 
        item_thumbnail = os.path.join(os.getcwd(), "kakao_image", "{}.png".format(item_id))
        item_synopsis = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")
        
        # get element and mouse wheel down
        elm = driver.find_element(By.XPATH, "//main[@class='h-full pt-0']")
        wheel_element(elm, 120)
        time.sleep(1)
        
        # click detail button
        driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-medium-white !whitespace-nowrap']").click()
        time.sleep(1)
        
        # get detail info
        item_title = driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word mt-8 s22-semibold-white']").text
        item_artist_list = driver.find_elements(By.XPATH, "//div[@class='flex mb-7']")
        item_artist_list.pop()
        item_artist = ""
        for i in range(len(item_artist_list)):
            item_artist_temp = item_artist_list[i].find_element(By.XPATH, "./dd").text
            if i == 0:
                item_artist += item_artist_temp
            else:
                if item_artist.find(item_artist_temp) != -1: # prevent duplicate
                    continue
                item_artist += "," + item_artist_temp
        
        item_adult = False
        date_finish_temp = driver.find_elements(By.XPATH, "//div[@class='mx-20 -mt-2']/div[1]/*") # div가 
        data_string = ""
        for date_element in date_finish_temp:
            if date_element.get_attribute("alt") == "성인":
                item_adult = True
            else:
                data_string += date_element.text
        item_date, item_finish_status = find_date(data_string, "완결", False)
        
        item_synopsis = item_synopsis.replace("'", "\\'")
        item_artist = item_artist.replace("'", "\\'")
        item_title = item_title.replace("'", "\\'")
        
        # item_etc_status = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [item_id, item_genre, item_address, item_rank, item_thumbnail, 
                                      item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    return webtoon_data_dict

# def multip(shared_dict, url_list, genre_list, cookie_list):
def multip(shared_dict, url_list, genre_list):
    pool = Pool(1) # kakao 멀티프로세싱 x
    for i in range(len(genre_list)):  #len(genre_list)
        pool.apply_async(collect_webtoon_data, args =(shared_dict, url_list, genre_list[i], i))
    pool.close()
    pool.join()   
    
################# 

if __name__ == '__main__':
    start = time.time()
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')
    table_name = Path(__file__).stem + now
    # file = open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w")
    genre_list = ["fantasy+drama", "romance", "school+action+fantasy", "romance+fantasy", "action+historical", "drama", "horror/thriller", "comic/daily"] # 사이트별 설정 
    base_url = "https://webtoon.kakao.com/ranking"
    
    #### manually ### 
    #### get login session cookie ####
    # driver = driver_set()
    # get_url_untill_done(driver, "https://webtoon.kakao.com/")
    # time.sleep(50) # time for login
    # cookie_list = driver.get_cookies()
    # pickle.dump(cookie_list, open(os.path.join(os.getcwd(), "module", "cookies", "{}_cookie.pkl".format(Path(__file__).stem)),"wb"))    
    # driver.close()

    # multi-processing
    manager = Manager()
    shared_dict = manager.dict()
    multip(shared_dict, base_url, genre_list)
    shared_dict_copy = shared_dict.copy()
    # json.dump(shared_dict_copy, file, separators=(',', ':'))
    # file.close()
    mydb = mysql_db("webtoon_db"+ now)
    mydb.create_table(table_name)
    for dict_value in shared_dict_copy.values():
        mydb.insert_to_mysql(dict_value, table_name)
    mydb.db.commit()
    
    print("{} >> ".format(Path(__file__).stem), time.time() - start)