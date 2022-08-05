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

print(db["platform"].find_one({'_id': ObjectId('62eccfe2b3699529a5a76f7e')})['update_time'])
print(type(db["platform"].find_one({'_id': ObjectId('62eccfe2b3699529a5a76f7e')})['update_time']))

a = datetime.datetime.now()
print(type(a))
print(type(a.isoformat()))
