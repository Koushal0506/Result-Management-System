from pymongo import MongoClient
from config import Config

_client = None

class SafeCollection:
    def __init__(self, name): self.name = name
    def find(self, *args, **kwargs):
        class Cursor(list):
            def sort(self, *a, **k): return self
            def limit(self, *a, **k): return self
        return Cursor([])
    def find_one(self, *args, **kwargs): return None
    def insert_one(self, *args, **kwargs): return None
    def update_one(self, *args, **kwargs): return None
    def delete_one(self, *args, **kwargs): return None
    def delete_many(self, *args, **kwargs): return None
    def count_documents(self, *args, **kwargs): return 0
    def distinct(self, *args, **kwargs): return []
    def drop(self): pass

class SafeDB:
    def __getattr__(self, name): return SafeCollection(name)
    def __getitem__(self, name): return SafeCollection(name)

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=10000, connectTimeoutMS=10000)
    return _client

def get_db():
    try:
        client = get_client()
        return client[Config.DB_NAME]
    except Exception as e:
        print(f"[MongoDB Notice] {e}")
        return SafeDB()

def check_connection():
    try:
        client = get_client()
        client.admin.command('ping')
        return True, "Connected to MongoDB Atlas"
    except Exception as e:
        return False, str(e)
