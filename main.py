import os
import time
import subprocess
import pymongo
import datetime
import json
from pymongo import MongoClient
from pathlib import Path

class mongo_item:
    update_time = datetime.datetime.now().isoformat()
    def __init__(self, element): 
        # self.db = db
        self.platform_name = element[0]
        self.item_id = element[1]
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
        # self.now = update_time
    
    def update_genre(db, *args):
        res = []
        for i in args:
            res += i
        res = list(set(res))
        for i in res:
            db["genre"].update_one(
                {"name" : i},
                {'$set' : {"name" : i}},
                upsert=True
            )
            
    def update_date(db, arg = []):
        for i in arg:
            db["date"].update_one(
                {"date" : i},
                {'$set' : {"date" : i}},
                upsert=True
            )
            
    def validate_date(self, db):
        date_obj = []
        for date in self.date.split(","):
            if db["date"].find_one({'date' : date}) == None: # date doesn't exist, such as "None", ""
                if self.finish_status == "연재":
                    date = "연재"
                else: 
                    date = "완결" 
            date_obj.append(db["date"].find_one({'date' : date})['_id'])
        return date_obj
        
            
    def update_webtoon(self, db):
        genre_obj = []
        for genre in self.genre_list:   
            genre_obj.append(db["genre"].find_one({'name' : genre})['_id'])
        
        # if webtoon already exists, only update platform
        # 장르랑 date도 바꿔야하지 않을까?
        # date는 플랫폼 기준으로 따로 저장할까? 연재처마다 연재요일 다를수 있으니까
        webtoon_exist = db["webtoon"].find_one({'title': self.title})
        if webtoon_exist : 
            # 만약 연재중이던게 완결나면?
            # 썸네일 바뀌면?
            # 장르 추가 => update_platform
            webtoon_id = webtoon_exist['_id']
            
        # if webtoon doesn't exist, create
        else: 
            date_obj = self.validate_date(db)
            # create webtoon
            self.webtoon = db["webtoon"].insert_one({
                'title' : self.title,
                'thumbnail' : self.thumbnail,
                'synopsis' : self.synopsis,
                'finish_status' : self.finish_status,
                'adult' : self.adult,
                'date' : date_obj, # obj list[]
                'genre' : genre_obj, # obj list[]
                'platform' : [],
                'artist': []
                })
            webtoon_id = self.webtoon.inserted_id  # type(self.webtoon) <class 'pymongo.results.InsertOneResult'>
            
        self.update_artist(db, webtoon_id) 
            
        self.update_platform(db, webtoon_id, genre_obj)
            
    
    def update_artist(self, db, webtoon_id): 
        # add webtoon to work_list
        for artist_temp in self.artist_name.split(","):
            artist_temp = artist_temp.strip()
            artist_exist = db["artist"].find_one({'name': artist_temp})
            # if artist already exists
            if artist_exist: 
                # update artist worklist
                db["artist"].update_one(
                    {"name" : artist_temp},
                    {"$addToSet" : {"work_list" : webtoon_id}}
                )
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$addToSet" : {"artist" : artist_exist['_id']}}
                )
            
            # if artist doesn't exist
            else:
                # create artist document
                self.artist = db["artist"].insert_one({ 
                    'name' : artist_temp,
                    'work_list' : [webtoon_id]
                })
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$addToSet" : {"artist" : self.artist.inserted_id}}
                )
        
    
    # 2022.8.5 플랫폼에 랭크차트 추적용 크롤링 날짜 추가
    def update_platform(self, db, webtoon_id, genre_obj):
        for i in range(len(genre_obj)):
            platform_temp = db["platform"].insert_one({
                'name' : self.platform_name,
                'genre' : genre_obj[i],
                'rank' : self.rank[i],
                'webtoon' : webtoon_id,
                'address' : self.address,
                'update_time' : mongo_item.update_time,
            })
            # add genre and platform into webtoon document
            db["webtoon"].update_one(
                {"_id" : webtoon_id},
                {"$addToSet" : {"platform" : platform_temp.inserted_id}}
                # "genre" : genre_obj[i] : 없으면 아래에서 만들었을테니까
            )
            
    # def update_platform(self, db, webtoon_id, genre_obj):
    #     # webtoon is in a platform collection
    #     if db["platform"].find_one({'webtoon' : webtoon_id, 'name' : self.platform_name}) : 
    #         webtoon_in_platform = db["platform"].find({'webtoon' : webtoon_id, 'name' : self.platform_name})
    #         counter = 0
    #         for platform_document in webtoon_in_platform: # check all existent webtoon
    #             if platform_document['genre'] in genre_obj: # if genre is same, update rank
    #                 db["platform"].update_one(
    #                     {"_id" : platform_document['_id']},
    #                     {"$set" : {"rank" : self.rank[counter]}}             
    #                 )
    #             else: # if this genre doesn't exist, create
    #                 platform_temp = db["platform"].insert_one({
    #                     'name' : self.platform_name,
    #                     'genre' : platform_document['genre'],
    #                     'rank' : self.rank[counter],
    #                     'webtoon' : webtoon_id,
    #                     'address' : self.address
    #                 })
    #                 # add genre into webtoon document
    #                 db["webtoon"].update_one(
    #                     {"_id" : webtoon_id},
    #                     {"$addToSet" : {"platform" : platform_temp.inserted_id}}
    #                 )
    #             counter += 1      
    #         # 만약 webtoon이 platform에 아예 없으면 추가하고, 만약 존재한다면 순위 업데이트 하거나 새로 추가
    #         # 기존 장르에서 빠지거나 하는건 생각을 당장 할필요 없어보이는게, 아예 장르에서 사라지지 않는 한, 랭킹이 낮아지는건 커버 되니까.
        
    #     # webtoon doesn't exist 
    #     else: 
    #         for i in range(len(genre_obj)):
    #             platform_temp = db["platform"].insert_one({
    #                 'name' : self.platform_name,
    #                 'genre' : genre_obj[i],
    #                 'rank' : self.rank[i],
    #                 'webtoon' : webtoon_id,
    #                 'address' : self.address
    #             })
    #             # add genre and platform into webtoon document
    #             db["webtoon"].update_one(
    #                 {"_id" : webtoon_id},
    #                 {"$addToSet" : {"platform" : platform_temp.inserted_id}}
    #                 # "genre" : genre_obj[i] : 없으면 아래에서 만들었을테니까
    #             )

if __name__ == '__main__':
    start = time.time()
    # tasks = ['bomtoon.py']
    tasks = ['bomtoon.py', 'ktoon.py', 'mrblue.py', 'toomics.py', 'naver.py']
    # orignial tasks = ['bomtoon.py', 'kakao_page.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestroy.py', 'toomics.py', 'kakao_webtoon.py']

    ## Multiprocessor-Crawling ##
    # process_list = []
    # for task in tasks:
    #     process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)]))
    # for p in process_list:
    #     time.sleep(0.5)
    #     p.wait()
    # print("total crawling time >> ", time.time() - start)  
    
    # store json file into mongodb 
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')    
    CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    mydb = client["react_test"]
    
    # field_tag = ['platform', 'item_id', 'genre', 'address', 'rank', 'thumbnail', 'title', 'date', 'finish_status', 'synopsis', 'artist', 'adult']
    # for task in tasks:
    #     converted_list = []
    #     platform_name = task[:-3]
    #     with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(platform_name))) as file:
    #         file_data = json.load(file)
    #         for element in file_data.values():
    #             element.insert(0, platform_name)
    #             converted_list.append(dict(zip(field_tag, element)))
    #     # mydb["webtoon"+ now].insert_many(converted_list)
    #     mydb["pedia_demo"].insert_many(converted_list)
    
    
    naver = ["daily", "comic", "fantasy", "action", "drama", "pure", "sensibility", "thrill", "historical", "sports"]
    bomtoon = ["bl", "romance"] 
    ktoon = ["romance", "bl/gl", "gag", "drama", "daily", "fantasy/SF", "sensibility", "action", "thrill/horror", "school"]
    mrblue = ["romance", "bl", "erotic", "drama", "gl", "action", "fantasy", "thriller"] 
    toomics = ["school/action", "fantasy", "drama", "romance", "gag", "sports", "historical", "horror/thrill", "bl"] 
    toomics_adult = ["drama", "romance", "fantasy", "ssul",  "horror/thrill", "sports","bl"] 
    kakao_webtoon = ["fantasy+drama", "romance", "school+action+fantasy", "romance+fantasy", "action+historical", "drama", "thrill/horror", "comic/daily"] 
    kakao_page = ["fantasy", "drama", "romance", "romance+fantasy", "historical", "bl"]  # 소년 = fantasy
    onestory = ["romance", "bl", "drama", "action", "fantasy", "daily", "gag", "thrill","adult"] 
    
    
    mongo_item.update_genre(mydb, ktoon, bomtoon , mrblue,toomics, naver, toomics_adult)
    mongo_item.update_genre(mydb, bomtoon)
    mongo_item.update_date(mydb, ["월","화","수","목","금","토","일","연재","완결","열흘"])
    
    
    #  {
    #    "ktoon" : {
    # 			"taskFile" : "ktoon.py",
    #      "genre" : [ sex ],
    # 		},
    #    ...
    #  }
    #  tasks = map upper json key value
    
    
    try: 
        for task in tasks:
            platform_name = task[:-3]
            with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(platform_name))) as file:
                file_data = json.load(file)
                for element in file_data.values():
                    element.insert(0, platform_name)
                    # print(element)
                    temp = mongo_item(element)
                    temp.update_webtoon(mydb)
    except Exception as e:
        print(e)
        print(temp.title)
    
    # 나중에 수동으로 중복처리 몇개해야됨
    # 위에 클래스 설정은 다른 파일로 빼자
                
    print("total process time >> ", time.time() - start)  