from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(base_url, genre_list, genre_name, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    count = 0 
    # 완전판, 전연령, 성인판 구분할지?    
    for genre_tag in genre_list:
        get_url_untill_done(driver, base_url)
        driver.find_element(By.XPATH, "//select[@class='arrow type']/option[@value='{}']".format(genre_tag)).click()
        time.sleep(10)
        # driver.findElement(By.xpath("//select/option[@value='1']")).click();
        genre_tag = genre_name[count]
        count+=1
        webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
        webtoon_data_dict.update(get_element_data(webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    item_id_list = []
    item_address_list = []
    item_rank = 0
    
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        item_address = webtoon_elements[i].find_element(By.XPATH, "parent::a").get_attribute("href")
        item_id = item_address[38:]
        item_id_list.append(item_id)
        item_address_list.append(item_address)    
        item_rank += 1
        
        webtoon_data_dict[item_id] = []
        webtoon_data_dict[item_id].append(genre_tag)
        webtoon_data_dict[item_id].append(item_id)
        webtoon_data_dict[item_id].append(item_address)
        webtoon_data_dict[item_id].append(item_rank)        

    for j in range(len(webtoon_elements)):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
        get_url_untill_done(driver, item_address_list[j])
        
        item_title = driver.find_element(By.ID, "bt-comic-name").text
        item_artist = driver.find_element(By.CLASS_NAME, "author").text.replace("&",",") # & -> ,
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='kv']/span").get_attribute("style")
        item_thumbnail = item_thumbnail[item_thumbnail.index('"')+1:-3]
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='head']/span").text, "완결", True, ["열흘"])
        item_synopsis = driver.find_element(By.CSS_SELECTOR, "#comic_desc").text
        # item_etc_status = driver.find_element(By.XPATH, "")
               
        webtoon_data_dict[item_id_list[j]].append(item_title)
        webtoon_data_dict[item_id_list[j]].append(item_artist)
        webtoon_data_dict[item_id_list[j]].append(item_thumbnail)
        webtoon_data_dict[item_id_list[j]].append(item_date)
        webtoon_data_dict[item_id_list[j]].append(item_finish_status)
        webtoon_data_dict[item_id_list[j]].append(item_synopsis)
        
    return webtoon_data_dict

################################################################################
start = time.time()
file = open(os.getcwd() + "/sab-git-test/json/{}.json".format(Path(__file__).stem), "w")
driver = driver_set()

login_url = "https://www.bomtoon.com/"
get_url_untill_done(driver, login_url)
time.sleep(2)
driver.find_elements(By.CLASS_NAME, "popCb")[1].click()
time.sleep(2)


user_id = "tpa74231@gmail.com"
user_pw = "Fortest111!!!"
login_for_adult(driver,login_url,By.CSS_SELECTOR,".btn-menu", By.ID,"user_id","user_pw")

genre_list = [4, 3] # 사이트별 설정 
genre_name = ["bl", "romance"] 
base_url = "https://www.bomtoon.com/main/rank"
css_tag = ".cont"



json.dump(collect_webtoon_data(base_url, genre_list, genre_name, css_tag), file, separators=(',', ':'))
print("time :", time.time() - start)    

driver.close()
driver.quit()
file.close()    