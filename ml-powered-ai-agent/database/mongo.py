# db.py
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "diabetes_app")

_client = MongoClient(MONGO_URI)
_db = _client[DB_NAME]

def get_db():
    return _db