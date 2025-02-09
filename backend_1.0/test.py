import os
from pymongo import MongoClient


# client = MongoClient(os.getenv("MONGODB_URI"))
client = MongoClient(
    "mongodb+srv://dzheng4m:cGqGXWHSHFQRxSRZ@cluster0.06nr7.mongodb.net/")


db = client.get_database('SecurityFilterDb')
lessons_collection = db.get_collection('Lesson')

print("Still woirkd")
