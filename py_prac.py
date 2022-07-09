from collector_setting import *
import json
from pathlib import Path


url = "https://webtoon.kakao.com/ranking"
driver = driver_set()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

time.sleep(100)