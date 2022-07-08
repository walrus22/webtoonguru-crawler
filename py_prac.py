from collector_setting import *
import json
from pathlib import Path


url = "https://webtoon.kakao.com/ranking"
driver = driver_set()
get_url_untill_done(driver, url)

# print(driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content"))
# driver.find_element(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word overflow-hidden text-ellipsis !whitespace-nowrap s22-semibold-white leading-33 mb-1']")

webtoon_elements = driver.find_elements(By.XPATH, "//div[@class='relative responsive-cell']/div/div/a") # webtoon element selection. 
count = 0
# print(len(webtoon_elements))

genre_click_list = driver.find_elements(By.XPATH, "//p[@class='whitespace-pre-wrap break-all break-words support-break-word s14-bold-white light:text-black !whitespace-nowrap']")

for i in range(len(genre_click_list)):
    genre_click_list[i].click()
    print(driver.find_elements(By.XPATH, "//div[@class='hardwareAccel w-full h-full absolute']/*")[0].get_attribute("alt") == "성인")


# for elements in webtoon_elements:
#     print(len(elements.find_elements(By.XPATH, ".//div[@class='w-full absolute left-0 bottom-10']/*")))
#     if len(elements.find_elements(By.XPATH, ".//div[@class='w-full absolute left-0 bottom-10']/*")) > 1 and elements.find_elements(By.XPATH, ".//div[@class='w-full absolute left-0 bottom-10']/div/*")[0].get_attribute("class") == "mx-2":
#         print("성인")
    
    # if len(elements.find_elements(By.XPATH, ".//div[@class='w-full absolute left-0 bottom-10']/*")) > 1 and elements.find_element(By.XPATH, ".//div[@class='w-full absolute left-0 bottom-10']/div/child").get_attribute("class") == "mx-2"
    
    # print(count)
    


time.sleep(10)