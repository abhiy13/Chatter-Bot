import sys
from pymongo import MongoClient
from pprint import pprint
sys.path.insert(0, '../rating_fetch/')
# sys.path.insert(0, './')
import cc, cf, hr
MongoURI = 'mongodb://abhishek:abhishek1@ds247290.mlab.com:47290/chatter_bot_db'
client = MongoClient(MongoURI)
db = client['chatter_bot_db'] 

users = db['users']

def update():
  find = users.find()
  for use in find:
    cc = use['codechef']
    cf = use['codeforces']
    c_r = cc.get_rating(cc)
    cf_r = cf.get_rating(cf)
    r = 4 * c_r + 6 * cf_r
    use['rating'] = r;
    users.save(use)
  
