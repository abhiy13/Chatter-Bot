from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['database'] 

users = db['users']

def refresh():
  find = users.find().sort('rating', 1)
  GM, M, E = 0, 0, 0
  for i in find:
    if 
