import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys # 이동해야 하는 경우 등 키입력시 사용
from webdriver_manager.chrome import ChromeDriverManager

def driver_set():
    options = Options()
    # options.add_argument("--incognito")
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chrome_options=options, executable_path="C:/Windows/chromedriver.exe") #win 집 업데이트.. webdriver 다시..
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(300)
    return driver

def get_url_untill_done(driver_var, url):
    count = 1
    for i in range(1, 6):
        try:
            driver_var.get(url)
            print(url + " << " + str(count) + " time try, success!")
            break
        except Exception as e:
            print(str(e) + " << " + url + str(count) + " time try")
            time.sleep(5)
            count+=1
            if i == 5:
                raise
            continue     

def find_date(item_date_temp : str, end_comment): # , day_keyword=False "요일" 있으면 True
    daylist = ["월", "화", "수", "목", "금", "토", "일"]
    item_date = ""
    if item_date_temp.find(end_comment) != -1: # end_comment = 완료?
        item_date = "완결"
        item_finish_status = "완결"
    else:
        item_finish_status = "연재"
        for d in daylist:
            if item_date_temp.find(d) != -1:
                item_date += d  
                
    return item_date, item_finish_status               
#                 if d == "일" and day_keyword==True :
#                     if day_keyword==True:
                        
                    
                
#                 if day_keyword == True:
#                     if d == "일" and item_date_temp.find("day_keyword") == -1: # 만약 일 위치가 마지막이면 무시 
#                         # ktoon: day_keyword = 일 요일
#                         # mrblue: day_keyword = 
#                         break
#                     item_date += d   
