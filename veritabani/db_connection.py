from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_db():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri)
    db = client["sosyalmedya"]
    return db
