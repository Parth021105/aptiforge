from pymongo import MongoClient
import os

MONGO_URI = os.environ.get('MONGO_URI','mongodb://localhost:27017/aptiforge')
EMAIL = 'parth123@gmail.com'
NEW_ROLE = 'admin'

client = MongoClient(MONGO_URI)
default_db = client.get_default_database()
db = default_db if default_db is not None else client['aptiforge']
res = db.users.update_one({'email': EMAIL}, {'$set': {'role': NEW_ROLE}})
print('matched', res.matched_count, 'modified', res.modified_count)
print('Promoted', EMAIL, 'to', NEW_ROLE)
