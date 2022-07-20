import os
import time
import subprocess
import pymongo
import datetime
import json
from pymongo import MongoClient
from pathlib import Path


if __name__ == '__main__':
    start = time.time()
    tasks = ['bomtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    # tasks = ['naver.py']
    # orignial tasks = ['bomtoon.py', 'kakao_page.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py', 'kakao_webtoon.py']

    process_list = []
    for task in tasks:
        process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
    for p in process_list:
        time.sleep(0.5)
        p.wait()
    print("total crawling time >> ", time.time() - start)  
    
    # store json to mongodb 
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')    
    CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    mydb = client["webtoon_db"+ now]
    field_tag = ['item_id', 'genre', 'address', 'rank', 'thumbnail', 'title', 'date', 'finish_status', 'synopsis', 'artist', 'adult']
    
    for task in tasks:
        converted_list = []
        with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(task[:-3]))) as file:
            file_data = json.load(file)
            for element in file_data.values():
                converted_list.append(dict(zip(field_tag, element)))
        mydb[task[:-3] + now].insert_many(converted_list)
    
    print("total process time >> ", time.time() - start)  
