from pymongo import MongoClient
import os
uri = os.environ.get('MONGO_URI','mongodb://localhost:27017/aptiforge')
print('Using MONGO_URI:', uri)
client = MongoClient(uri)
# select db from URI if present, else 'aptiforge'
default_db = client.get_default_database()
db = default_db if default_db is not None else client['aptiforge']
print('Database:', db.name)
for u in db.users.find():
    print(u)
