from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['test-database'] 

users = db['users']
print(users)

# test = {
#   'codechef': 'abhiy13',
#   'codeforces': 'abhiy13',
#   'rating': 0,
#   'discord': '123'
# }
'''
result = users.insert_one(test);

if result.acknowledged:
  print("Data Written with id ", result.inserted_id)
'''
#finds all users
find = users.find().sort('rating')
for use in find:
  cc = use['codechef']
  cf = use['codeforces']
  c_r = 
