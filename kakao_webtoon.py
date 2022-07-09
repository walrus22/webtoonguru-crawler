from collector_setting import *
import json
from pathlib import Path
from urllib.request import urlopen
from PIL import Image


################################# function setting ############################
def collect_webtoon_data(base_url, genre_list):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    webtoon_elements_url = []
    genre_click_list = driver.find_elements(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-bold-white light:text-black !whitespace-nowrap']")
    
    for i in range(len(genre_list)):
        # 클릭 이동
        genre_click_list[i].click()
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
        
        foreground = Image.open(urlopen(driver.find_element(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/picture/source[2]").get_attribute("srcset"))).convert("RGBA")
        background = Image.open(urlopen(driver.find_element(By.XPATH, "//picture[@class='bg-content-home']/source").get_attribute("srcset"))).convert("RGBA")
        background.paste(foreground, (20, 75), foreground)
        img = background.crop((0,0,750,750))
        img.save('/Users/kss/Documents/GitHub/sab-git-test/kakao_image/{}.png'.format(item_id))
        item_thumbnail = open('/Users/kss/Documents/GitHub/sab-git-test/kakao_image/{}.png'.format(item_id), 'r')
        
        title_temp = driver.find_element(By.XPATH, "//div[@class='overflow-hidden cursor-pointer']/p[1]")
        item_title = title_temp.text
        item_synopsis = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")
        item_artist = driver.find_element(By.XPATH, "//div[@class='overflow-hidden cursor-pointer']/p[2]").text
        # time.sleep(1)
        title_temp.click()
        # time.sleep(1)
        
        date_finish_temp = driver.find_elements(By.XPATH, "//div[@class='mx-20 -mt-2']/div/p")
        if len(date_finish_temp) == 1 :
            item_finish_status = "완결"
        else:
            item_finish_status = "연재"
            item_date = date_finish_temp[1].text
        
        # item_etc_status = driver.find_element(By.XPATH, "")
        webtoon_data_dict[item_id] = [genre_tag, item_id, item_address, item_rank, item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist]

################################################################################
start = time.time()
file = open(os.getcwd() + "/sab-git-test/json/{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

genre_list = ["fantasy+drama", "romance", "school+action+fantasy", "romance+fantasy", "action+historical", "drama", "horror/thriller", "comic/daily"] # 사이트별 설정 
base_url = "https://webtoon.kakao.com/ranking"
# css_tag = ""

# 장르 = 클릭으로 이동
login_url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26state%3Db3MuMTY1NzM0MzI1NDc2MnRSTzJHRU82a1g5NVg3TWdxV0kxNzUzdUluNkJ6R01zekpvYVNoMjR6TlF5azVJdzZm%26redirect_uri%3Dhttps%253A%252F%252Fgateway-kw.kakao.com%252Fauth%252Fv1%252Foauth%252Fkakao%252Fcode%26prompt%3Dlogin%26client_id%3Da4c06dc3e5dd447ffff35a303bea612e"
get_url_untill_done(driver, login_url)

user_id = "tuntunjun@naver.com"
user_pw = "Zmfhffldxptmxm123!@#"
id_tag = "//input[@name='email']"
pw_tag = "//input[@name='password']"

login_for_adult(driver, user_id, user_pw, id_tag, pw_tag)
get_url_untill_done(driver, base_url)


json.dump(collect_webtoon_data(base_url, genre_list), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()