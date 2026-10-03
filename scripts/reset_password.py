from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os

MONGO_URI = os.environ.get('MONGO_URI','mongodb://localhost:27017/aptiforge')
EMAIL = 'parth123@gmail.com'
NEW_PW = 'Test1234'

client = MongoClient(MONGO_URI)
default_db = client.get_default_database()
db = default_db if default_db is not None else client['aptiforge']
hashed = generate_password_hash(NEW_PW)
res = db.users.update_one({'email': EMAIL}, {'$set': {'password': hashed}})
print('matched', res.matched_count, 'modified', res.modified_count)
print('New password for', EMAIL, 'is', NEW_PW)
