from operator import ge
import os
from platform import platform
import time
import subprocess
import pymongo
import datetime
import json
from pymongo import MongoClient
from pathlib import Path
import collections

class item:
    def __init__(self, element): 
        # self.db = db
        self.platform_name = element[0]
        # 1: item_id
        self.genre_list = element[2]
        self.address = element[3]
        self.rank = element[4]
        self.thumbnail = element[5]
        self.title = element[6]
        self.date = element[7]
        self.finish_status = element[8]
        self.synopsis = element[9]
        self.artist_name = element[10]
        self.adult = element[11]
    
    def update_platform(self, db, webtoon_id, genre_obj):
        webtoon_in_platform = db["platform"].find({'webtoon' : webtoon_id, 'name' : self.platform_name}) # list
        # webtoon is in a platform collection
        if webtoon_in_platform : 
            counter = 0
            for platform_document in webtoon_in_platform: # check all existent webtoon
                if platform_document['genre'] in genre_obj: # if genre is same, update rank
                    db["platform"].update_one(
                        {"_id" : platform_document['_id']},
                        {"$set" : {"rank" : self.rank[counter]}}             
                    )
                else: # if this genre doesn't exist, create
                    platform_temp = db["platform"].insert_one({
                        'name' : self.platform_name,
                        'genre' : platform_document['genre'],
                        'rank' : self.rank[counter],
                        'webtoon' : webtoon_id,
                        'address' : self.address
                    })
                    # add genre into webtoon document
                    db["webtoon"].update_one(
                        {"_id" : webtoon_id},
                        {"$push" : {"platform" : platform_temp.inserted_id}}
                    )
                counter += 1      
            # 만약 webtoon이 platform에 아예 없으면 추가하고, 만약 존재한다면 순위 업데이트 하거나 새로 추가
            # 기존 장르에서 빠지거나 하는건 생각을 당장 할필요 없어보이는게, 아예 장르에서 사라지지 않는 한, 랭킹이 낮아지는건 커버 되니까.
        
        # webtoon doesn't exist 
        else: 
            for i in range(len(genre_obj)):
                platform_temp = db["platform"].insert_one({
                    'name' : self.platform_name,
                    'genre' : genre_obj[i],
                    'rank' : self.rank[i],
                    'webtoon' : webtoon_id,
                    'address' : self.address
                })
                # add genre into webtoon document
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$push" : {"platform" : platform_temp.inserted_id}}
                )
    
    def update_webtoon(self, db):
        genre_obj = []
        for genre in self.genre_list:   
            genre_obj.append(db["genre"].find_one({'name' : genre})['_id'])
        
        # if webtoon already exists, only update platform
        # 장르랑 date도 바꿔야하지 않을까?
        # date는 플랫폼 기준으로 따로 저장할까?
        webtoon_exist = db["webtoon"].find_one({'title': self.title}) 
        if webtoon_exist : 
            # 만약 연재중이던게 완결나면?
            # 썸네일 바뀌면?
            # platform update
            pass
            
        # if webtoon doesn't exist, create
        else: 
            date_obj = []
            for date in self.date.split(","):
                date_obj.append(db["date"].find_one({'date' : date})['_id'])

            # create webtoon
            self.webtoon = db["webtoon"].insert_one({
                'title' : self.title,
                'thumbnail' : self.thumbnail,
                'synopsis' : self.synopsis,
                'finish_status' : self.finish_status,
                'adult' : self.adult,
                'date' : date_obj, # obj list
                'genre' : genre_obj, # obj list
                'platform' : []
                })
            
            # print(type(self.webtoon)) #<class 'pymongo.results.InsertOneResult'>
            
            # if artist already exists
            artist_exist = db["artist"].find_one({'name': self.artist_name})
            if artist_exist:
                # update artist worklist
                db["artist"].update_one(
                    {"name" : self.artist_name},
                    {"$push" : {"work_list" : self.webtoon.inserted_id}}
                )
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : self.webtoon.inserted_id},
                    {"$set" : {"artist" : artist_exist['_id']}}
                )
            
            # if artist doesn't exist
            else:
                # create artist document
                self.artist = db["artist"].insert_one({ 
                    'name' : self.artist_name,
                    'work_list' : [self.webtoon.inserted_id]
                })
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : self.webtoon.inserted_id},
                    {"$set" : {"artist" : self.artist.inserted_id}}
                )
            
            self.update_platform(db, self.webtoon.inserted_id, genre_obj)
            
            # # platform create    
            # for i in range(len(genre_obj)):
            #     platform_temp = db["platform"].insert_one({
            #         'name' : self.platform_name,
            #         'genre' : genre_obj[i],
            #         'rank' : self.rank[i],
            #         'webtoon' : self.webtoon.inserted_id,
            #         'address' : self.address
            #     })
            #     db["webtoon"].update_one(
            #         {"_id" : self.webtoon.inserted_id},
            #         {"$push" : {"platform" : platform_temp.inserted_id}}
            #     )
            

            
                
            
    
        

start = time.time()
tasks = ['bomtoon.py', 'toomics.py']
# tasks = ['bomtoon.py', 'ktoon.py', 'mrblue.py', 'onestory.py', 'toomics.py']
# orignial tasks = ['bomtoon.py', 'kakao_page.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py', 'kakao_webtoon.py']

# process_list = []
# for task in tasks:
#     process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
# for p in process_list:
#     time.sleep(0.5)
#     p.wait()
# print("total crawling time >> ", time.time() - start)  

# store json to mongodb 
# now = datetime.datetime.now().strftime('_%Y%m%d_%H')    
# CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
# client = MongoClient(CONNECTION_STRING)
# mydb = client["dividetest"]
# field_tag = ['platform', 'item_id', 'genre', 'address', 'rank', 'thumbnail', 'title', 'date', 'finish_status', 'synopsis', 'artist', 'adult']
    

# a.update_webtoon()

CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
client = MongoClient(CONNECTION_STRING)
mydb = client["dividetest"]

# with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format('bomtoon'))) as file:
#     file_data = json.load(file)
    # for element in file_data.values():
    #     element.insert(0, 'bomtoon')
a = item(['ktoon', '10714', ['drama', 'daily', 'sensibility'], 'https://v2.myktoon.com/web/works/list.kt?worksseq=10714', [4, 5, 3], 'https://cds.myktoon.com/download?file=/img/webtoon/thumb/2020/03/31/1585614182615.jpg', '썸툰 시즌3', '화,목', '연재', '설레는 매 순간 내 곁에는 언제나 네가 있었다.한 번쯤은 들어봤을 너와 나, 우리 모두의 이야기.', '모히또모히칸', False])
a.update_webtoon(mydb)
b = item(['baver', 'asdd', ['romance', 'bl'], 'https://v2.sad.com/web/works/list.kt?worksseq=10714', [1, 2], 'https://cds.myktoon.com/downl20/03/31/1585614182615.jpg', '썸툰 시즌3', '화,목', '연재', '설레는 매 순간 내 곁에는 언제나 네가 있었다.한기.', '모히또모히칸', False])
b.update_webtoon(mydb)        

        
    
        # for element in file_data.values():
    
    # for task in tasks:
    #     converted_list = []
    #     platform_name = task[:-3]
    #     with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(platform_name))) as file:
    #         file_data = json.load(file)
    #         for element in file_data.values():
    #             element.insert(0, platform_name)
    #             # converted_list.append(dict(zip(field_tag, element)))
    #             print(element)
        # mydb["webtoon"+ now].insert_many(converted_list)
        # mydb["pedia_demo"].insert_many(converted_list)
    
    
