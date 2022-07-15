import os
import time
import random
from PIL import Image
from urllib.request import urlopen
from selenium import webdriver
from multiprocessing import Pool, Manager

from collector_setting import *
import json
from pathlib import Path

################################# function setting ############################
def collect_webtoon_data(url, genre_tag, css_tag):
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't') # creat new tab. 이동해야 하는 경우 사용
    webtoon_data_dict={}
    driver = driver_set()
    get_url_untill_done(driver, url)
    webtoon_elements = driver.find_elements(By.CSS_SELECTOR, css_tag) # webtoon element selection. 
    webtoon_data_dict.update(get_element_data(driver, webtoon_elements, genre_tag))
    return webtoon_data_dict
    
def get_element_data(driver, webtoon_elements, genre_tag):
    webtoon_data_dict = {}
    item_rank = 0
    item_address_list = []
    item_id_list = []
    
    for i in range(len(webtoon_elements)): # len(webtoon_elements)
        item_address = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        item_id = item_address[31:]
        item_id_list.append(item_id)
        item_address_list.append(item_address)    
        item_rank += 1
        
        # address_temp = webtoon_elements[i].find_element(By.XPATH, "./a").get_attribute("href")
        # item_id = address_temp[12:]
        # item_address = "https://www.mrblue.com" + address_temp
        # 아니씨발이게 맥이랑 가져오는 형식이 다른가?
        # 윈도우에선 address_temp가 전체 주소를 가져오고, mac에선 안가져왔는데 ㅡㅡ 씨발 
        # 7.8 뭐야 맥북에서도 전체주소 가져오네 ㅡㅡ
        # 근본없는 사이트다운 주소 태그다
        
        webtoon_data_dict[item_id] = []
        webtoon_data_dict[item_id].append(genre_tag)
        webtoon_data_dict[item_id].append(item_id)
        webtoon_data_dict[item_id].append(item_address)
        webtoon_data_dict[item_id].append(item_rank)
        
    for j in range(len(webtoon_elements)):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        get_url_untill_done(driver, item_address_list[j])
        
        item_title = driver.find_element(By.CLASS_NAME, 'title').text
        item_date, item_finish_status = find_date(driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[1]").text, "완결", False)
        item_thumbnail = driver.find_element(By.XPATH, "//div[@class='img-box']/p/img").get_attribute("src")
        # item_etc_status = 
        # synopsis
    
        # 그림/글 : 1명 // 그림 ~명 글 ~명 2가지 케이스 있다
        item_artist = ""
        first = True
        for author in driver.find_elements(By.CLASS_NAME, 'authorname'):
            if first == True:
                first = False
            else:
                item_artist += ","
        
        webtoon_data_dict[item_id_list[j]].append(item_title)
        webtoon_data_dict[item_id_list[j]].append(item_date)
        webtoon_data_dict[item_id_list[j]].append(item_thumbnail)
        # webtoon_data_dict[item_id_list[j]].append(item_etc_status)
        webtoon_data_dict[item_id_list[j]].append(item_finish_status)
        webtoon_data_dict[item_id_list[j]].append(item_artist)
        
    return webtoon_data_dict

################################################################################



# driver = driver_set()
# url = "https://webtoon.kakao.com/content/%ED%99%94%ED%8F%90%EA%B0%9C%ED%98%81/1877"
# get_url_untill_done(driver, url)


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
    raise error

driver = driver_set()
get_url_untill_done(driver, "https://webtoon.kakao.com/content/%EC%95%84%EB%B9%84%EB%AC%B4%EC%8C%8D/1395", 5, 7)

item_artist = driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word overflow-hidden text-ellipsis !whitespace-nowrap s12-regular-white -mt-3 opacity-85 leading-21 h-21 pr-45']").text


fore_temp = driver.find_elements(By.XPATH, "//div[@class='overflow-hidden absolute inset-0']/*")[0]
if fore_temp.tag_name == "video":
    foreground = Image.open(urlopen(fore_temp.get_attribute("poster"))).convert("RGBA")
else :
    foreground = Image.open(urlopen(fore_temp.find_element(By.XPATH, "./img").get_attribute("src"))).convert("RGBA")
background = Image.open(urlopen(driver.find_element(By.XPATH, "//picture[@class='bg-content-home']/source").get_attribute("srcset"))).convert("RGBA")
background.paste(foreground, (20, 150), foreground) # fore: 710x600 , back: 750x13??
img = background.crop((0,0,750,750))
img.save(os.path.join(os.getcwd(), "kakao_image", "{}.png".format("test"))) 
item_thumbnail = os.path.join(os.getcwd(), "kakao_image", "{}.png".format("test"))
item_synopsis = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")



# get element and mouse wheel down
elm = driver.find_element(By.XPATH, "//main[@class='h-full pt-0']")
wheel_element(elm, 120)
time.sleep(1)
# click detail button
driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-medium-white !whitespace-nowrap']").click()
time.sleep(1)

item_title = driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word mt-8 s22-semibold-white']").text
# item_artist_list = driver.find_elements(By.XPATH, "//div[@class='flex mb-7']")
# item_artist_list.pop()
# item_artist = ""
# for i in range(len(item_artist_list)):
#     if i == 0:
#         item_artist += item_artist_list[i].find_element(By.XPATH, "./dd").text
#     else:
#         item_artist += "," + item_artist_list[i].find_element(By.XPATH, "./dd").text     

item_adult = False
date_finish_temp = driver.find_elements(By.XPATH, "//div[@class='mx-20 -mt-2']/div[1]/*") # div가 
data_string = ""
for date_element in date_finish_temp:
    if date_element.get_attribute("alt") == "성인":
        item_adult = True
    else:
        data_string += date_element.text
item_date, item_finish_status = find_date(data_string, "완결", False)
driver.close()

print(item_synopsis)