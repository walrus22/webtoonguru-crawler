import os
import time
import datetime
import subprocess
import mysql.connector
from pathlib import Path


if __name__ == '__main__':
    start = time.time()
    tasks = ['bomtoon.py', 'kakao_page.py', 'kakao_webtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    # tasks = ['bomtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    
    # create mysql DB
    # 이거 숨겨야겠는데..
    webtoon_db = mysql.connector.connect(    
        host="localhost",
        user="root",
        password="Zmfhffldxptmxm123!@#"
        datab
    )
    db_cursor = webtoon_db.cursor()
    db_cursor.execute("CREATE DATABASE {}".format("webtoon_db"+ datetime.datetime.now().strftime('_%Y%m%d_%H')))    
    
    process_list = []
    for task in tasks:
        process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
    for p in process_list:
        time.sleep(0.5)
        p.wait()
    print("total process time >> ", time.time() - start)  
