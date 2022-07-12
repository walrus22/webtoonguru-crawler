import subprocess
import os
import time

if __name__ == '__main__':
    start = time.time()
    # tasks = ['bomtoon.py', 'kakao_page.py', 'kakao_webtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    tasks = ['bomtoon.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py']
    process_list = []
    for task in tasks:
        process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
    for p in process_list:
        p.wait()
    print("time :", time.time() - start)  
