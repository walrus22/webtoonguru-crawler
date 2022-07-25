import os
from platform import platform
import time
import subprocess
import pymongo
import datetime
import json
from pymongo import MongoClient
from pathlib import Path


start = time.time()
tasks = ['bomtoon.py', 'toomics.py']

CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
client = MongoClient(CONNECTION_STRING)
mydb = client["dividetest"]
    
    # with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format("ktoon"))) as file:
    #     file_data = json.load(file)
    #     for element in file_data.values():
    #         element.insert(0, "ktoon")
    #         print(element)



# print(a)
# print(type(a))

# if a:
#     print("hi")
# else: 
#     print("no")

class k:     
    def __init__(self):
        self.n = 1
    def a(self) : 
        print("hi")
        self.b()
    def b(self):
        print("hello")
    def c(self):
        self.m = 2
        print(self.m)
        
# a = k()
# a.c()
    
        
        
# a = mydb["webtoon"].find_one({'title': "썸툰 시즌3"})
# from bson.objectid import ObjectId
# webtoon_in_platform = mydb["platform"].find({'webtoon': ObjectId('62de559446c1f6eaa046f314'), 'name' : 'ktoon'}) # list

# for document in webtoon_in_platform:
#     print(document)
#     print(webtoon_in_platform)
['bomtoon.py', 'ktoon.py', 'mrblue.py', 'onestory.py', 'toomics.py']
ktoon = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
bomtoon = ["bl", "romance"] 
mrblue = ["romance", "bl", "erotic", "drama", "gl", "action", "fantasy", "thriller"] 
toomics = ["school/action", "fantasy", "drama", "romance", "gag", "sports", "historical", "horror/thrill", "bl"] 
naver = ["daily", "comic", "fantasy", "action", "drama", "pure", "sensibility", "thrill", "historical", "sports"]
res = list(set(ktoon + bomtoon + mrblue + toomics + naver))
print(res)