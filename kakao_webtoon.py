from collector_setting import *
import json
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
from multiprocessing import Pool 


################################# function setting ############################
def collect_webtoon_data(base_url, genre_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    for i in range(len(genre_list)): #
        # 클릭 이동
        webtoon_elements_url = []
        get_url_untill_done(driver, base_url)
        time.sleep(1)        
        genre_click_list = driver.find_elements(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-bold-white light:text-black !whitespace-nowrap']")
        genre_click_list[i].click()
        time.sleep(1)
        webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='relative responsive-cell']/div/div/a") # webtoon element selection. 
        for elements in webtoon_elements:
            webtoon_elements_url.append(elements.get_attribute("href"))
        webtoon_elements_url.insert(0, driver.find_element(By.XPATH, "//a[@class='relative w-full h-full opacity-0 z-2 animate-fadeIn']").get_attribute("href"))
        webtoon_data_dict.update(get_element_data(webtoon_elements_url, genre_list[i]))
    return webtoon_data_dict

    
def get_element_data(webtoon_elements_url, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    
    for item_address in webtoon_elements_url: # len(webtoon_elements)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address)
        
        item_id = item_address[item_address.rfind("/")+1:]
        item_rank += 1
        
        fore_temp = driver.find_elements(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/*")[0]
        if fore_temp.tag_name == "video":
            foreground = Image.open(urlopen(fore_temp.get_attribute("poster"))).convert("RGBA")
        else :
            foreground = Image.open(urlopen(fore_temp.find_element(By.XPATH, "./img").get_attribute("src"))).convert("RGBA")
        background = Image.open(urlopen(driver.find_element(By.XPATH, "//picture[@class='bg-content-home']/source").get_attribute("srcset"))).convert("RGBA")
        background.paste(foreground, (20, 150), foreground) # fore: 710x600 , back: 750x13??
        img = background.crop((0,0,750,750))
        img.save(os.path.join(os.getcwd(), "kakao_image", "{}.png".format(item_id))) 
        # img.save('/Users/kss/Documents/GitHub/sab-git-test/kakao_image/{}.png'.format(item_id)) # mac 위에거로 될꺼임 아마
        # item_thumbnail = open('/Users/kss/Documents/GitHub/sab-git-test/kakao_image/{}.png'.format(item_id), 'r')  # mac
        
        item_thumbnail = os.path.join(os.getcwd(), "kakao_image", "{}.png".format(item_id))
        title_temp = driver.find_element(By.XPATH, "//div[@class='overflow-hidden cursor-pointer']/p[1]")
        item_title = title_temp.text
        item_synopsis = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")
        item_artist = driver.find_element(By.XPATH, "//div[@class='overflow-hidden cursor-pointer']/p[2]").text
        time.sleep(random.uniform(1,2))
        title_temp.click()
        time.sleep(random.uniform(0,1))
        
        itme_adult = False
        date_finish_temp = driver.find_elements(By.XPATH, "//div[@class='mx-20 -mt-2']/div[1]/*") # div가 
        data_string = ""
        for date_element in date_finish_temp:
            if date_element.get_attribute("alt") == "성인":
                itme_adult = True
            else:
                data_string += date_element.text
        item_date, item_finish_status = find_date(data_string, "완결", False)
        
        # item_etc_status = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [genre_tag, item_id, item_address, item_rank, item_thumbnail, item_title, 
                                      item_date, item_finish_status, item_synopsis, item_artist, itme_adult]
        #, 
        
    return webtoon_data_dict
################################################################################
start = time.time()

file = open(os.path.join(os.getcwd(), "json", "{}test.json".format(Path(__file__).stem)), "w")
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing']))
# driver = driver_set() 

genre_list = ["fantasy+drama", "romance", "school+action+fantasy", "romance+fantasy", "action+historical", "drama", "horror/thriller", "comic/daily"] # 사이트별 설정 
base_url = "https://webtoon.kakao.com/ranking"
# css_tag = ""

get_url_untill_done(driver, base_url)

json.dump(collect_webtoon_data(base_url, genre_list), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()