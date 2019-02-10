class Env:
  def __init__(self):
    self.BOT_TOKEN = 'NTM1NDQ5NDI5ODY0NjExODQw.DzMRqA.9ROgoqNKXnS7fhwRDyb3ak-jGBM'
    self.MONGO_URI = 'mongodb://abhishek:abhishek1@ds247290.mlab.com:47290/chatter_bot_db'
  
  def get_bot_token(self):
    return self.BOT_TOKEN
  
  def get_bot_uri(self):
    return self.MONGO_URI