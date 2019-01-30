import sys
from pymongo import MongoClient
from pprint import pprint
sys.path.insert(0, '../rating_fetch/')
# sys.path.insert(0, './')
import cc, cf

MongoURI = 'Your URI'
client = MongoClient(MongoURI)
db = client['chatter_bot_db'] 

users = db['users']

def createUser(discord_id, cci, cfi):
  c_r = cc.get_rating(cci)
  if c_r == -1:
    return "Codechef Handle Not found"
  cf_r = cf.get_rating(cfi)
  if cf_r == -1:
    return "Codeforces Handle Not found"
  r = 4 * int(c_r) + 6 * int(cf_r) 
  print(c_r, cf_r, r)
  use = {
    'codechef' : cci,
    'codeforces' : cfi,
    'rating': r,
    'discord': discord_id
  }
  result = users.insert_one(use)
  if result.acknowledged:
    return "Records Updated !"
  else:
    return "Sorry Some error Occured !"
  
