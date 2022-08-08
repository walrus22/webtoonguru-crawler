import os
from platform import platform
import time
import subprocess
import pymongo
import datetime
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from pathlib import Path


# tasks = ['bomtoon.py', 'toomics.py']

CONNECTION_STRING = "mongodb+srv://sab:Zmfhffldxptmxm123%21%40%23@sabmongo.uy5i9.mongodb.net/test"
client = MongoClient(CONNECTION_STRING)
db = client["react_test"]


# artist_temp = "9".strip()
# print('^{}$'.format(artist_temp))
# artist_exist = db["artist"].find_one({'name': {'$regex' : '^{}$'.format(artist_temp), "$options" : "i"}})
# print(artist_exist)


author = "엠스토리허브(별땅, 연실), 하하(잉어), 호호, 헤헤, 엠스토리허브(별땅, 123,연실)"
author1 = "하이, 키키"
# print(author.split(","))

# if author.index("(") != -1 and author.index(",") > author.index("(") and author.index(",") < author.index(")"):
#     author = author.replace(",", "/")
    
import re

item_artist= []
item_artist += re.split(r',\s*(?![^()]*\))', author)
item_artist += re.split(r',\s*(?![^()]*\))', author1)
print(item_artist)