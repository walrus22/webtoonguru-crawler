import os
import time
import subprocess
# import pymongo
import datetime
import json
from pymongo import MongoClient
from pathlib import Path
from PIL import Image
import boto3
import requests
from io import BytesIO

class mongo_item:
    def __init__(self, element, update_time): 
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
        self.artist_list = element[10]
        self.adult = element[11]
        self.update_time = update_time
    
    # def update_genre(db, *args):
    def update_genre(db, genre_list, genre_list_kor):
        # res = []
        # for i in args:
        #     res += i
        # res = list(set(res))
        # for i in res:
        #     db["genre"].update_one(
        #         {"name" : i},
        #         {'$set' : {"name" : i}},
        #         upsert=True
        #     )
        
        for i in range(len(genre_list)):
            db["genre"].update_one(
                {"name" : genre_list[i]},
                {'$set' : {"name" : genre_list[i], "name_kor": genre_list_kor[i]}},
                upsert=True
            )
        
        
            
    def update_date(db, arg = []):
        for i in arg:
            db["date"].update_one(
                {"name" : i},
                {'$set' : {"name" : i}},
                upsert=True
            )
            
    def validate_date(self, db):
        date_obj = []
        for date in self.date.split(","):
            if db["date"].find_one({'name' : date}) == None: # date doesn't exist, such as "None", ""
                if self.finish_status == "연재":
                    date = "비정기"
                else: 
                    date = "완결" 
            date_obj.append({
                "_id": db["date"].find_one({'name' : date})['_id'],
                "name": date,
                })
        return date_obj
        
            
    def update_webtoon(self, db):
        genre_obj = []
        for genre in self.genre_list:   
            genre_obj.append({
                "_id": db["genre"].find_one({'name' : genre})['_id'],
                "name" : genre,
                })
        
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
            
            response = requests.get(self.thumbnail)
            s3.put_object(
                Body=BytesIO(response.content),
                Bucket=S3_BUCKET_NAME,
                Key=str(webtoon_id),
            )

            
            
        self.update_artist(db, webtoon_id) 
        self.update_platform(db, webtoon_id, genre_obj)
            
    
    def update_artist(self, db, webtoon_id): 
        # add webtoon to work_list
        for artist_temp in self.artist_list:
            artist_temp = artist_temp.strip().replace("*", "\*")
            
            # 8.7 작가명 case insensitive
            artist_exist = db["artist"].find_one({'name': {'$regex' : '^{}$'.format(artist_temp), "$options" : "i"}})
            
            # if artist already exists
            if artist_exist: 
                # update artist worklist
                db["artist"].update_one(
                    {"name" : artist_temp},
                    {"$addToSet" : 
                        {"work_list" : 
                            {'_id' : webtoon_id,
                             'name' : self.title}
                        }
                    }
                )
                
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$addToSet" : {"artist" : {"_id" : artist_exist['_id'], "name" : artist_exist['name']}}}
                )
            
            # if artist doesn't exist
            else:
                # create artist document
                self.artist = db["artist"].insert_one({ 
                    'name' : artist_temp,
                    'work_list' : [{'_id' : webtoon_id, 'name' : self.title}]
                })
                # create webtoon artist field
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$addToSet" : {"artist" : {"_id" : self.artist.inserted_id, "name" : artist_temp}}}
                )
        
    
    # 2022.8.5 플랫폼에 랭크차트 추적용 크롤링 날짜 추가
    def update_platform(self, db, webtoon_id, genre_obj):
        # webtoon is in the platform collection
        if db["platform"].find_one({'webtoon._id' : webtoon_id, 'name' : self.platform_name}) : 
            webtoon_in_platform = db["platform"].find({'webtoon._id' : webtoon_id, 'name' : self.platform_name})
            counter = 0
            for platform_document in webtoon_in_platform: # check all existent webtoon
                print(genre_obj)
                print(platform_document)
                print(platform_document['genre'])
                
                if platform_document['genre'] in genre_obj: # if genre is same, update rank
                    db["platform"].update_one(
                        {"_id" : platform_document['_id']},
                        {"$set" : {"rank" : self.rank[counter],
                                   'update_time' : self.update_time}}             
                    )
                else: # if this genre doesn't exist, create
                    platform_temp = db["platform"].insert_one({
                        'name' : self.platform_name,
                        'genre' : platform_document['genre'],
                        'rank' : self.rank[counter],
                        'webtoon' : {"_id": webtoon_id, "name": self.title},
                        'address' : self.address,
                        'update_time' : self.update_time,
                    })
                    # add genre into webtoon document
                    db["webtoon"].update_one(
                        {"_id" : webtoon_id},
                        {"$addToSet" : {"platform" : {"_id" : platform_temp.inserted_id, "name": self.platform_name}}}
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
                    'webtoon' : {"_id": webtoon_id, "name": self.title},
                    'address' : self.address,
                    'update_time' : self.update_time,
                })
                # add genre and platform into webtoon document
                db["webtoon"].update_one(
                    {"_id" : webtoon_id},
                    {"$addToSet" : {"platform" : {"_id" : platform_temp.inserted_id, "name": self.platform_name}}}
                    # "genre" : genre_obj[i] : 없으면 아래에서 만들었을테니까
                )
            
        for i in range(len(genre_obj)):
            platform_history_temp = db["platform_history"].insert_one({
                'name' : self.platform_name,
                'genre' : genre_obj[i],
                'rank' : self.rank[i],
                'webtoon' : {"_id": webtoon_id, "name": self.title},
                'address' : self.address,
                'update_time' : self.update_time,
            })


if __name__ == '__main__':
    start = time.time()
    update_time = datetime.datetime.now().isoformat()
    
    s3 = boto3.client('s3')
    S3_BUCKET_NAME = 'webtoonguru-thumbnail-jjy'

    # tasks = ['ktoon.py']
    tasks = ['bomtoon.py', 'ktoon.py', 'mrblue.py', 'toomics.py', 'naver.py', 'lezhin.py', 'onestory.py']
    # orignial tasks = ['bomtoon.py', 'kakao_page.py', 'ktoon.py', 'lezhin.py', 'mrblue.py', 'naver.py', 'onestory.py', 'toomics.py', 'kakao_webtoon.py']

    ### Multiprocessor Crawling ##
    process_list = []
    for task in tasks:
        # process_list.append(subprocess.Popen(["python", os.path.join(os.getcwd(), "module", task)])) # win
        process_list.append(subprocess.Popen(["python3", os.path.join(os.getcwd(), "module", task)])) # mac
    for p in process_list:
        time.sleep(0.5)
        p.wait()
    print("total crawling time >> ", time.time() - start)  
    
    # store json file into mongodb 
    now = datetime.datetime.now().strftime('_%Y%m%d_%H')    
    CONNECTION_STRING = os.environ['MONGO_URI']
    client = MongoClient(CONNECTION_STRING)
    mydb = client["0830"]
    
    genre_list = ["romance", "bl", "gl", "drama", "daily", "action", "gag", "fantasy", 
                  "thrill+horror", "historical", "sports", "sensibility", "school", "erotic"]
    genre_list_kor = ["로맨스", "BL", "GL", "드라마", "일상", "액션", "개그", "판타지", 
                  "스릴/공포", "무협", "스포츠", "감성", "학교", "에로"]
    
    # day_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun", ""]
    day_list_kor = ["월","화","수","목","금","토","일","연재","완결","열흘", "비정기"]
    
    mongo_item.update_genre(mydb, genre_list, genre_list_kor)
    mongo_item.update_date(mydb, day_list_kor)
    
    
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
                    temp = mongo_item(element, update_time)
                    temp.update_webtoon(mydb)
    except Exception as e:
        print(e)
        print(temp.title)
    
    # 나중에 수동으로 중복처리 몇개해야됨
    # 위에 클래스 설정은 다른 파일로 빼자
    
    print("total process time >> ", time.time() - start)  
    
    