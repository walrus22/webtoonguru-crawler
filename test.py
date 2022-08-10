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
db = client["react_test2"]


# artist_temp = "9".strip()
# print('^{}$'.format(artist_temp))
# artist_exist = db["artist"].find_one({'name': {'$regex' : '^{}$'.format(artist_temp), "$options" : "i"}})
# print(artist_exist)

a= [
  {
    "_id": "62efb7ebf41d4a941f192139",
    "date": "목"
  },
  {
    "_id": "62efb7ebf41d4a941f192155",
    "date": "일"
  }
]

b = {
    "_id": "62efb7ebf41d4a941f192139",
    "date": "목"
  }


print(b in a)


# print(type(db["genre"].find_one({'name' : "romance"})['_id']))