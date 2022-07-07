from collector_setting import *
import json
from pathlib import Path
driver = driver_set()

# get_url_untill_done(driver, "https://www.mrblue.com/webtoon/wt_000051664") 
# get_url_untill_done(driver, "https://www.mrblue.com/webtoon/wt_000051344") 
get_url_untill_done(driver, "https://www.mrblue.com/webtoon/wt_000047383") 


item_title = driver.find_element(By.CLASS_NAME, 'title').text
# item_date = 
# item_thumbnail = 
# item_etc_status = 
# item_finish_status =
        
# 그림/글 : 1명 // 그림 ~명 글 ~명 2가지 케이스 있다
item_artist = ""
first = True
for author in driver.find_elements(By.CLASS_NAME, 'authorname'):
    
    if first == True:
        first = False
    else:
        item_artist += ","
    item_artist += author.text.replace(" ", "")

a, b= find_date(driver.find_element(By.XPATH, "//div[@class='txt-info']/div/p[2]/span[1]").text, "완결")
  
print(a)
print(b)
    

print(item_title)
print(item_artist)

# print(item_)
# print(item_)
# print(item_)
# print(item_)
# print(item_)

 