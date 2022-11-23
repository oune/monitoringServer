from pymongo import MongoClient

client = MongoClient(host='localhost', port=27017)

db = client['sensors']
db.datas.insert_one({'test': 'hello'})

print(db.datas)