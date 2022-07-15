import os
import time
import subprocess
# import datetime
# from pathlib import Path


if __name__ == '__main__':
    start = time.time()
    tasks = ['bomtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    # orignial tasks = ['bomtoon.py', 'kakao_page.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py', 'kakao_webtoon.py']

    process_list = []
    for task in tasks:
        process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
    for p in process_list:
        time.sleep(0.5)
        p.wait()
    print("total process time >> ", time.time() - start)  



    