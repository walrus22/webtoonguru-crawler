from pymongo import MongoClient

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
    
    collection_name = dbname["user_1_items"]
    
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
    
    item_details = collection_name.find()
    # for item in item_details:
    #     # This does not give a very readable output
    #     print(item)
    #     # print(item['item_name'], item['category'])
        
    from pandas import DataFrame
    items_df = DataFrame(item_details)
    # 야 신기하네 한번 for loop 돌리니까 item_details 비어버림    
    

    print(items_df)