class Env:
  def __init__(self):
    self.BOT_TOKEN = 'Your BOT_TOKEN'
    self.MONGO_URI = 'Your MONGO_URI'
  
  def get_bot_token(self):
    return self.BOT_TOKEN
  
  def get_bot_uri(self):
    return self.MONGO_URI