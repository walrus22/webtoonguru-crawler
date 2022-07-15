from pymongo import MongoClient
from pandas import DataFrame

def get_database():
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    
    collection_name = dbname["123"]
    
    # item_1 = {
    # "_id" : "U1IT00001",
    # "item_name" : "Blender",
    # "max_discount" : "10%",
    # "batch_number" : "RR450020FRG",
    # "price" : 340,
    # "category" : "kitchen appliance"
    # }

    # item_2 = {
    # "_id" : "U1IT00002",
    # "item_name" : "Egg",
    # "category" : "food",
    # "quantity" : 12,
    # "price" : 36,
    # "item_description" : "brown country eggs"
    # }
    # collection_name.insert_many([item_1,item_2])
    
    # from dateutil import parser
    # expiry_date = '2021-07-13T00:00:00.000Z'
    # expiry = parser.parse(expiry_date)
    # item_3 = {
    # "item_name" : "Bread",
    # "quantity" : 2,
    # "ingredients" : "all-purpose flour",
    # "expiry_date" : expiry
    # }
    # collection_name.insert_one(item_3)
    
    # item_details = collection_name.find()
    # # for item in item_details:
    # #     # This does not give a very readable output
    # #     print(item)
    # #     # print(item['item_name'], item['category'])
        
    # items_df = DataFrame(item_details)
    # 야 신기하네 한번 for loop 돌리니까 item_details 비어버림    
    
    # webtoon_data_dict[item_id] = [item_id, item_genre, item_address, str(item_rank), item_thumbnail, item_title, 
    #                                   item_date, item_finish_status, item_synopsis, item_artist, item_adult]
    
    
    # webtoon_data_dict = {
    #     '1142414': ['1142414', 'romance', 'https://1313.com', '12', 'https://123.com', '마왕어쩌구', '월,화', '연재', '마왕군이 처들어왓다', '나나니니', True],
    #     '23232': ['23232', 'dfsf', 'https://1313.com', '12', 'https://123.com', 'kk', '월,화', '연재', '마왕군이 처들어왓다', '나나니니', True]
    # }
    
    # # print(webtoon_data_dict)
    

    # field_tag = ['item_id', 'item_genre', 'item_address', 'item_rank', 'item_thumbnail', 'item_title', 'item_date', 'item_finish_status', 'item_synopsis', 'item_artist', 'item_adult']
    # test_dict=[]
    
    # for element in webtoon_data_dict.values():
    #     test_dict.append(dict(zip(field_tag, element)))
        
    # print(test_dict)

    # collection_name.insert_many(test_dict)
    # item_details = collection_name.find()
    # items_df = DataFrame(item_details)

    # print(items_df)
    
    st1 = "드링커스하이15세이상"
    print(st1.find("세이상"))
    print(st1[:-5])
    