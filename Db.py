import os
import pymongo

class Db:
    def __init__(self):
        db_uri = os.environ.get('DATABASE_URI', 'mongodb://127.0.0.1:27017/db')
        
        client = pymongo.MongoClient(db_uri)
        
        self.db = client.get_default_database()
    

db = Db().db