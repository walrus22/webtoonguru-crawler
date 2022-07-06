from collector_setting import *
import json
import time
from pathlib import Path


driver = driver_set()
# driver.get("https://www.myktoon.com/web/webtoon/works_list.kt?genreseq=123")
driver.get("https://www.myktoon.com/web/webtoon/works_list.kt?genreseq=123&orderbyfg=search&&pageNo=2")

driver.implicitly_wait(3)
ele = driver.find_elements(By.CLASS_NAME, "next")
if len(ele) == 0:
    print("hi")

driver.close()
driver.quit()