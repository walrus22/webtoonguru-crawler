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
db = client["dividetest"]
    


artist = ObjectId('62de87e761a518e1fc35e7ba')
gaecha = ObjectId('62de87e761a518e1fc35e7b9')
aa = ObjectId('62de881484a49e383ae8e2e4')

db["artist"].update_one(
    {"_id" : artist},
    {"$addToSet" : {"work_list" : gaecha}}
)


