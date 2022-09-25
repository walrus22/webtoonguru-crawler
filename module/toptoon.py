import urllib.request, json 
from collector_setting import *
import os
from pathlib import Path

genre_list = {
    "로맨스": "romance",
    "드라마": "drama",
    "일상": "daily",
    "감성": "sensibility",
    "코믹": "gag",
    "판타지": "fantasy",
    "공포,스릴러": "thrill+horror",
    "액션": "action",
    "무협": "historical",
    "학원": "school",
    "스포츠": "sports",
    "에로": "erotic",
    "bl": "BL",
    "gl": "GL",
    }

# day_list_kor = ["월","화","수","목","금","토","일","연재","완결","열흘", "비정기"]

with urllib.request.urlopen("https://dl-app-api.toptoon.com/api/v1/comic/getComicsList") as url:
    data = json.load(url)
    for d in data["data"]:
        if d['id'] == "comicTotal":
            total_url = d['url']
            
with urllib.request.urlopen(total_url) as url:
    data = json.load(url)
    with open(os.path.join(os.getcwd(), "module", "json", "{}.json".format(Path(__file__).stem)), "w") as out:
        webtoon_data_dict = {}
        webtoon_data_dict_temp = {}
        for item in data:
            # print('-----------------------------------')
            # print(item)
            item_id = item['id']
            
            # genre 없는 애들이 너무 많음
            item_genre=[]
            for genre in item['meta']['genre']:
                if genre_list.get(genre['name']):
                    item_genre.append(genre_list.get(genre['name']))
                    
            for genre in item['tag']:
                # print(genre['name'])
                if genre_list.get(genre['name']):
                    item_genre.append(genre_list.get(genre['name']))
                    
            # tag에도 장르 해당없으면 romance로 퉁
            if item_genre == []:
                item_genre = ["romance"]
                
            res = [*set(item_genre)] # 중복 제거
            # print(item_genre)

            item_address = "https://toptoon.com" + item['meta']['comicsListUrl']
            item_thumbnail = item['thumbnail']['landscape']
            item_title = item['meta']['title']
            
            item_finish_status = "완결" if item['meta']['type'][0] == "complete" else "연재"
            item_synopsis = item['meta']['description']
            
            item_artist = [x['name'] for x in item['meta']['author']['authorData']] if item['meta']['author'] != [] else []
            item_adult = True if item['meta']['adult'] == 1 else False
            item_rank = item['meta']['weeklyViewCount']
            item_date = "비정기"
            
            item_rank = [item_rank] * len(item_genre)
            
            # title 같은게 있어서 중복 제거용으로 이렇게함
            webtoon_data_dict_temp[item_title] = [item_id, item_genre, item_address, item_rank, item_thumbnail, item_title, item_date, item_finish_status, item_synopsis, item_artist, item_adult]
            

        # print(webtoon_data_dict_temp)
        webtoon_data_dict_sorted = sorted(webtoon_data_dict_temp.items(), key=lambda x: x[1][3][0], reverse=True)
        
        for i in range(len(webtoon_data_dict_sorted)):
            # rank 
            webtoon_data_dict_sorted[i][1][3] = [i+1] * len(webtoon_data_dict_sorted[i][1][3])
            # list to dict
            webtoon_data_dict[webtoon_data_dict_sorted[i][1][0]] = webtoon_data_dict_sorted[i][1]
        
        json.dump(webtoon_data_dict, out) 
        