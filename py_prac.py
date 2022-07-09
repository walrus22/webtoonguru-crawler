from collector_setting import *
import json
from pathlib import Path


# url = "https://webtoon.kakao.com/ranking"
# driver = driver_set()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# time.sleep(100)


def file_open():
    if os.getcwd()[2] == "\\":
        file =  open(os.getcwd() + "\\json\\{}.json".format(Path(__file__).stem), "w")
    else: 
        file = open(os.getcwd() + "/sab-git-test/json/{}.json".format(Path(__file__).stem), "w")
    return file
    
file = file_open()

